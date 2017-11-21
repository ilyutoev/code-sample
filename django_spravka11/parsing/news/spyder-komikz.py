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

from parsingfunct import data_change, create_img_folder, clean_text, copyright, rubrics_id, genshingle, compaire, write_news_to_db, last_ten_news_links, load_db_shingle,resize
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

stop_list = 'jdf Ракурс Мистика Мужчина и женщина История Авторские колонки Обратите внимание Только у нас Акценты Комикс Обзоры Дисконт Интервью В сети Кулинарные рецепты Полезные советы Дачные хлопоты Спрашивали? Отвечаем На здоровье'
exist_news_links = last_ten_news_links('komikz')

news = {} #словарь для хранения всех спарсенных палей, который записывается затем в базу данных
#exist_news_links = last_ten_news_links('bnkomi')
edem_dalshe = True #храним статус проверки уже спарсеных статей - если False - значит наткнулись на уже существующую статьи и дальше не парсим

img_anons_links = [] #список для хранения ссылок на картинки-аоносы

class KomikzSpider(Spider):
    initial_urls = ['http://komikz.ru/news/']
    base_url = 'http://komikz.ru/news'

    print('\n-- Парсинг komikz.ru - ' + str(datetime.datetime.now()))

    #переопределяем кодировку - без нее парсит пустые строки
    def create_grab_instance(self, **kwargs):
        grab = super(KomikzSpider, self).create_grab_instance(**kwargs)
        grab.setup(document_charset='cp1251', timeout=20, connect_timeout=20)
        return grab

    def task_initial(self, grab, task):        
        global edem_dalshe

        next_link = grab.doc.select('//div[@class="pagenavi clearfix"]/a[@class="prev"]') #ссылка на следующую страницу
        print(next_link.attr('href'))

        kz_links = grab.doc.select('//div[@class="list-news clearfix"]//h4/a')
        kz_rubrics = grab.doc.select('//div[@class="list-news clearfix"]//a[@class="cat"]')

        prior = 0
        for link, rubr in zip(kz_links, kz_rubrics):
            if exist_news_links.count(link.attr('href')):   #проверяем на уже спарсенные статьи
                edem_dalshe = False
            elif stop_list.find(rubr.text()) == -1: #проверка на стоп лист рубрик
                news = {
                    'url': link.attr('href'),
                    'rubr': rubrics_id(rubr.text(), 'komikz')
                }
                prior+=1
                yield Task('newspage', url=link.attr('href'), news=news, priority=prior)
        if edem_dalshe: #проверка идти ли на следующую страницу
            yield Task('initial', url=next_link.attr('href'), task_try_count=task.task_try_count + 1)

    def task_newspage(self, grab, task):
        task.news['title'] = clean_text(grab.doc.select('//div[@class="post-inner"]/h1').text(),'normal')
        task.news['date'] = data_change(grab.doc.select('//div[@class="newsdate"]').text(), 'komiinform')

        kz_text = grab.doc.select('//div[@class="post-inner"]').html()
        task.news['text'] = pur.feed(kz_text)   #очищаем от html тегов
        task.news['text'] = clean_text(task.news['text'],'normal')  #очищаем от юникод сиволов и пустых абзацев
        task.news['text'] = task.news['text'][task.news['text'].find('<p'):task.news['text'].rfind('</p>')+4]
        task.news['text'] = copyright(task.news['text'], 'komikz')
        task.news['text'] = re.sub(r'\s+', ' ', task.news['text']) #удаляем лишние пробелы
        
        task.news['shingle_text'] = genshingle(kz_text,10) #создаем шинглы текста
        task.news['shingle_title'] = genshingle(task.news['title'],2) #создаем шинглы тайтла

        net_povtora = True
        links, shingle_titles, shingle_texts = load_db_shingle(task.news['date'], 'komikz')
        temp_shin_text = json.loads(task.news['shingle_text'])
        temp_shin_title = json.loads(task.news['shingle_title'])
        for link, shingle_title, shingle_text in zip(links, shingle_titles, shingle_texts):
            if compaire(temp_shin_title,shingle_title) > 90 or compaire(temp_shin_text,shingle_text) > 60:
                net_povtora = False                
        if net_povtora:
            task.news['anons'] = task.news['text'][task.news['text'].find('<p>')+3:task.news['text'].find('</p>')]  #выделение первого абзаца текста для анонса

            #скачивание картинок
            kz_img = grab.doc.select('//div[@class="post-inner"]//img')
            task.news['img_anons'] = '' #обнуление объекта словаря
            img_text = []
            for i, elem in enumerate(kz_img):
                if elem.attr('src'):
                    path_to_img_folder = create_img_folder(task.news['date'])
                    img_name = md5(elem.attr('src').split("/")[-1].encode('utf-8')).hexdigest()[:15] + '.' + elem.attr('src').split(".")[-1].lower()
                    new_link_to_img = path_to_img_folder + '/' + img_name
                    if not os.path.exists(new_link_to_img):
                        fix_link = urllib.parse.quote(elem.attr('src'))#если в названиии файла пробел
                        yield Task('image', url=fix_link, priority=task.priority, path=new_link_to_img)
                    if i == 0:  #перавя картинка идет на анонс
                        #сохраняем в нужном формате cms instant + делаем 2 ресайза картинки
                        img_anons_links.append(new_link_to_img) #добавляем ссылку для проверки на скачивание

                        task.news['img_anons'] = new_link_to_img[new_link_to_img.find('media/')+6:]

                        img_text.append(urllib.parse.quote(elem.attr('src')) + ' ' + new_link_to_img)
                    else:
                        img_text.append(urllib.parse.quote(elem.attr('src')) + ' ' + new_link_to_img)

            #заменяем в тексте старые ссылки на картинки на новые-сгенерированные. Строим путь к папке как на сайте будет
            if img_text:
                for img in img_text:
                    link_images = img.split(' ')
                    task.news['text'] = task.news['text'].replace(link_images[0],'/media/' + link_images[1][link_images[1].find('media/')+6:])
            
            task.news['id_source'] = 4 #id источника парсинга - в данному случае комикз
            write_news_to_db(task.news) #Запись в базу


    def task_image(self, grab, task):
        grab.response.save(task.path)
        if img_anons_links.count(task.path) != 0:
            img_anons_links.remove(task.path)

def main():
    bot = KomikzSpider(thread_number=1)
    bot.run()

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()