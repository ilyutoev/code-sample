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
    'h2':[''],
    'p': [''], # разрешает все атрибуты у тега div
    'img':['src'],
    'iframe':['*'], #ролики с ютуба
    'table': ['*'],
    'tr': ['*'],
    'td': ['*'],
    # все остальные теги удаляются, но их содержимое остается
})

stop_list = 'jdjf Без купюр Видеовзгляд Делу время Жизнь в Коми Жизнь в стиле Tele2 Комментарии ПоTechи Фотовзгляд Интервью'
news = {} #словарь для хранения всех спарсенных палей, который записывается затем в базу данных
exist_news_links = last_ten_news_links('komionline')
edem_dalshe = True #храним статус проверки уже спарсеных статей - если False - значит наткнулись на уже существующую статьи и дальше не парсим
img_anons_links = [] #список для хранения ссылок на картинки-аоносы

class KomionlineSpider(Spider):
    initial_urls = ['http://komionline.ru/archive/']
    base_url = 'http://komionline.ru/archive/'
    print('\n-- Парсинг komionline.ru -  ' + str(datetime.datetime.now()))

    def create_grab_instance(self, **kwargs):
        grab = super(KomionlineSpider, self).create_grab_instance(**kwargs)
        grab.setup(timeout=20, connect_timeout=20)
        return grab

    def task_initial(self, grab, task):
        global edem_dalshe
        links = grab.doc.select('//div[@class="news"]/h1//a')
        next_link = grab.doc.select('//div[@style="clear: both; width: 100%; margin: 0 0 15px 0;"]/a[@style="float: right;"]')

        prior = 0 #переменная для генерации приоритета выполнения заданий
        for link in links:
            if exist_news_links.count(link.attr('href').replace('/news/','/news/print/')):   #проверяем на уже спарсенные статьи
                edem_dalshe = False
            else:
                prior+=1
                link = link.attr('href').replace('news', 'news/print')
                yield Task('newspage', url=link, priority=prior)
        
        if edem_dalshe: #проверка идти ли на следующую страницу
            print(next_link.attr('href'))
            yield Task('initial', url=next_link.attr('href'), task_try_count=task.task_try_count + 1)

    def task_newspage(self, grab, task):
        rubr = grab.doc.select('//h2[@id="navbar"]').text() #выделяем рубрику из хлебных крошек
        rubr = rubr.split(' ')[-1]
        if stop_list.find(rubr) == -1:
            news['url'] = task.url.replace('http://komionline.ru', '')
            news['rubr'] = rubrics_id(rubr, 'komionline')   #записыаем id рубрики
            news['title'] = clean_text(grab.doc.select('//h2[@class="title"]').text(),'normal')
            data = grab.doc.select('//p[@class="moreinfo"]').text()[:20]
            news['date'] = data.replace(',', '')
            text = grab.doc.select('//div[@class="text"]').html()
            news['text'] = clean_text(text,'normal')#очистка от спецсимволов
            news['text'] = pur.feed(news['text'])#очистка от тегов
            news['text'] = news['text'][news['text'].find('</h2>')+5:]#вырезаем заголовок из текста
            news['text'] = news['text'][:news['text'].rfind('<p>')]#вырезаем последний абзац
            news['text'] = copyright(news['text'], 'komionline')
            news['shingle_text'] = genshingle(text,10) #создаем шинглы текста
            news['shingle_title'] = genshingle(news['title'],2) #создаем шинглы тайтла

            net_povtora = True
            links, shingle_titles, shingle_texts = load_db_shingle(news['date'], 'komionline')
            temp_shin_text = json.loads(news['shingle_text'])
            temp_shin_title = json.loads(news['shingle_title'])
            for link, shingle_title, shingle_text in zip(links, shingle_titles, shingle_texts):
                if compaire(temp_shin_title,shingle_title) > 90 or compaire(temp_shin_text,shingle_text) > 60:
                    net_povtora = False                
            if net_povtora:
                news['anons'] = news['text'][news['text'].find('<p>')+3:news['text'].find('</p>')]  #выделение первого абзаца текста для анонса
                #скачивание изображений из статьи
                bn_img = grab.doc.select('//div[@id="printnews"]//img')
                news['img_anons'] = '' #обнуление объекта словаря
                img_text = []
                for i, elem in enumerate(bn_img):
                    if elem.attr('src'):
                        path_to_img_folder = create_img_folder(news['date'])
                        img_name = md5(elem.attr('src').split("/")[-1].encode('utf-8')).hexdigest()[:15] + '.' + elem.attr('src').split(".")[-1].lower()
                        new_link_to_img = path_to_img_folder + '/' + img_name
                        if not os.path.exists(new_link_to_img):
                            fix_link = urllib.parse.quote(elem.attr('src'))
                            yield Task('image', url=fix_link, priority=task.priority, path=new_link_to_img)
                        if i == 0:  #перавя картинка идет на анонс
                            img_anons_links.append(new_link_to_img) #добавляем ссылку для проверки на
                            #сохраняем в нужном формате cms instant
                
                            news['img_anons'] = new_link_to_img[new_link_to_img.find('media/')+6:]

                            img_text.append(urllib.parse.quote(elem.attr('src')) + ' ' + new_link_to_img)
                        else:
                            img_text.append(urllib.parse.quote(elem.attr('src')) + ' ' + new_link_to_img)

                #заменяем в тексте старые ссылки на картинки на новые-сгенерированные. Строим путь к папке как на сайту бедт
                if img_text:
                    for img in img_text:
                        link_images = img.split(' ')
                        news['text'] = news['text'].replace(link_images[0],'/media/' + link_images[1][link_images[1].find('media/')+6:])
                
                news['id_source'] = 3 #id источника парсинга - в данному случае комионлайн
                write_news_to_db(news) #Запись в базу

    def task_image(self, grab, task):
        grab.response.save(task.path)
        if img_anons_links.count(task.path) != 0:
            img_anons_links.remove(task.path) 

def main():
    bot = KomionlineSpider(thread_number=1)
    bot.run()

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()