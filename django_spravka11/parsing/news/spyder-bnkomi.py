# coding: utf-8
from grab import Grab
from grab.spider import Spider, Task
import logging
from purifier.purifier import HTMLPurifier
import os
from hashlib import md5

import sys
sys.path
sys.path.append('/home/spravka/projects/spravka11/spravka11/parsing/')

from parsingfunct import data_change, create_img_folder, clean_text, copyright, rubrics_id, genshingle, compaire, write_news_to_db, last_ten_news_links, load_db_shingle, resize
import re
import json
import urllib.parse
import datetime

pur = HTMLPurifier({
    'p': [''], # разрешает все атрибуты у тега div
    'img':['src'],
    'iframe':['*'], #ролики с ютуба
    'table': ['*'],
    'tr': ['*'],
    'td': ['*'],
    # все остальные теги удаляются, но их содержимое остается
})

stop_list = 'jdjf Опрос БНК Новости партнеров На обсуждение Фотокадр дня Видеоопрос БНК Народный корреспондент Из блогов'
news = {} #словарь для хранения всех спарсенных палей, который записывается затем в базу данных
exist_news_links = last_ten_news_links('bnkomi')
edem_dalshe = True #храним статус проверки уже спарсеных статей - если False - значит наткнулись на уже существующую статьи и дальше не парсим
img_anons_links = [] #список для хранения ссылок на картинки-аоносы

class BnkomiSpider(Spider):
    initial_urls = ['http://bnkomi.ru/']
    base_url = 'http://bnkomi.ru'
    print('\n-- Парсинг bnkomi.ru -  ' + str(datetime.datetime.now()))

    def create_grab_instance(self, **kwargs):
        grab = super(BnkomiSpider, self).create_grab_instance(**kwargs)
        grab.setup(timeout=20, connect_timeout=20)
        return grab
    
    def task_initial(self, grab, task):
        bn_rubrics = grab.doc.select('//h2[@class="title"]/span[@class="categorylink"]/a')
        bn_links = grab.doc.select('//h2[@class="title"]/a')
        prior = 0
        for rubric, link in zip(bn_rubrics, bn_links):
            rubric = rubric.text()
            if link.attr('href') in exist_news_links:   #проверяем на уже спарсенные статьи
                pass
            elif stop_list.find(rubric) == -1 and stop_list.find(link.text()) == -1: #проверка на стоп лист слов в заголовке и наличие рубрики
                news = {
                    'url': link.attr('href'),
                    'rubr': rubrics_id(rubric, 'bnkomi')
                    }
                prior+=1
                yield Task('newspage', url=link.attr('href'), news=news, priority=prior)

    def task_newspage(self, grab, task):
        task.news['title'] = clean_text(grab.doc.select('//h2[@class="title"]').text(),'normal')
        task.news['date'] = data_change(grab.doc.select('//div[@class="date"]').text(), 'bnkomi')

        bn_text = grab.doc.select('//div[@class="cnt daGallery"]').html()
        #разобраться с подписью к фото - или выделить и уадлить абзац, либо заменить один класс на другой
        task.news['text'] = pur.feed(bn_text)   #очищаем от html тегов
        task.news['text'] = clean_text(task.news['text'],'normal')  #очищаем от юникод сиволов и пустых абзацев
        task.news['text'] = copyright(task.news['text'], 'bnkomi')
        task.news['text'] = re.sub(r'\s+', ' ', task.news['text']) #удаляем лишние пробелы
        
        task.news['shingle_text'] = genshingle(bn_text,10) #создаем шинглы текста
        task.news['shingle_title'] = genshingle(task.news['title'],2) #создаем шинглы тайтла

        #проверка на одинаковые статьи по заголовку и текстам
        net_povtora = True
        links, shingle_titles, shingle_texts = load_db_shingle(task.news['date'], 'bnkomi')
        temp_shin_text = json.loads(task.news['shingle_text'])
        temp_shin_title = json.loads(task.news['shingle_title'])
        for link, shingle_title, shingle_text in zip(links, shingle_titles, shingle_texts):
            if compaire(temp_shin_title,shingle_title) > 90 or compaire(temp_shin_text,shingle_text) > 60:
                net_povtora = False                
        if net_povtora:
            task.news['anons'] = task.news['text'][task.news['text'].find('<p>')+3:task.news['text'].find('</p>')]  #выделение первого абзаца текста для анонса

            #скачивание изображений из статьи
            bn_img = grab.doc.select('//div[@class="cnt daGallery"]//img')
            task.news['img_anons'] = '' #обнуление объекта словаря
            img_text = []
            for i, elem in enumerate(bn_img):
                if elem.attr('src'):
                    path_to_img_folder = create_img_folder(task.news['date'])
                    img_name = md5(elem.attr('src').split("/")[-1].encode('utf-8')).hexdigest()[:15] + '.' + elem.attr('src').split(".")[-1].lower()
                    new_link_to_img = path_to_img_folder + '/' + img_name
                    if not os.path.exists(new_link_to_img):
                        fix_link = urllib.parse.quote(elem.attr('src'))#если в названиии файла пробел
                        yield Task('image', url=fix_link, priority=task.priority, path=new_link_to_img)
                    if i == 0:  #перавя картинка идет на анонс
                        img_anons_links.append(new_link_to_img) #добавляем ссылку для проверки на 
                        
                        task.news['img_anons'] = new_link_to_img[new_link_to_img.find('media/')+6:]

                        img_text.append(urllib.parse.quote(elem.attr('src')) + ' ' + new_link_to_img)
                    else:
                        img_text.append(urllib.parse.quote(elem.attr('src')) + ' ' + new_link_to_img)

            #заменяем в тексте старые ссылки на картинки на новые-сгенерированные. Строим путь к папке как на сайту бедт
            if img_text:
                for img in img_text:
                    link_images = img.split(' ')
                    task.news['text'] = task.news['text'].replace(link_images[0],'/media/' + link_images[1][link_images[1].find('media/')+6:])
            
            task.news['id_source'] = 2 #id источника парсинга - в данному случае бнкоми
            write_news_to_db(task.news) #Запись в базу


    def task_image(self, grab, task):
        grab.response.save(task.path)
        if img_anons_links.count(task.path) != 0:
            img_anons_links.remove(task.path)        

def main():
    bot = BnkomiSpider(thread_number=1)
    bot.run()

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()

'''
Добавлена проверка на повторы - вычисляются шинглы тайтала и текста статьи и если процент повтора больше определенной величины статья не пишеться в бд
'''