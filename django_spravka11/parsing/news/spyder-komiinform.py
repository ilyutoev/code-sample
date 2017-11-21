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

from parsingfunct import data_change, create_img_folder, clean_text, copyright, rubrics_id, genshingle, compaire, write_news_to_db, last_ten_news_links, resize
import urllib.parse #для преобразования уролв на картинки с русскими буквами в сиволы хекс
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

#в этот список загружаем последние спарсенные статьи из базы данных - урлы вида /news/123456/
exist_news_links = last_ten_news_links('komiinform')

stop_list = 'тест22 Неформат Пресс-релизы' #Стоп лист рубрик - чтобы не парсить эти статьи
news = {} #словарь для хранения всех спарсенных палей, который записывается затем в базу данных
img_anons_links = [] #список для хранения ссылок на картинки-аоносы

class KomiinformSpider(Spider):
    initial_urls = ['http://www.komiinform.ru/']
    base_url = 'http://www.komiinform.ru'
    print('\n-- Парсинг komiinform.ru - ' + str(datetime.datetime.now()))

    def create_grab_instance(self, **kwargs):
        grab = super(KomiinformSpider, self).create_grab_instance(**kwargs)
        grab.setup(timeout=20, connect_timeout=20)
        return grab

    def task_initial(self, grab, task):
        #получаем ссылку на следующую страницу с новостями

        prior = 0 #переменная для генерации приоритета выполнения заданий

        for news in grab.doc.select('//div[@class="row item"]'):

            url = news.select('.//a[@class="smallHeader2"]').attr('href')
            rubric = news.select('.//div[@class="information fix-bottom"]//a[contains(@href,"/e/")]').text()
            anons = news.select('.//p[@class="strip-content"]').text()
            
            if exist_news_links.count(url):   #проверяем на уже спарсенные статьи
                pass
            elif stop_list.find(rubric) == -1:   #проверка на стоп листе рубрик
                news = {
                    'url': url,
                    'rubr': rubrics_id(rubric, 'komiinform'),  #записыаем id рубрики
                    'anons': anons
                }
                prior+=1
                yield Task('newspage', url=url, news=news, priority=prior)


    def task_newspage(self, grab, task):
        task.news['title'] = clean_text(grab.doc.select('//h1').text(),'normal')
        task.news['date'] = data_change(grab.doc.select('//div[@class="addDate"]').text(), 'komiinform')

        ki_text = grab.doc.select('//div[@class="daGallery"][2]').html()

        lll = grab.doc.select('//div[@class="daGallery"][1]/div[@class="newsImage"]/a')

        task.news['link_anons_img'] = ''
        if lll:
            task.news['link_anons_img'] = lll.attr('href')

        #выделяем текст из новости по признаку абзацев - ищем первый <p> и последний </p> и делаем срез
        ki_text = ki_text[ki_text.find('<p'):ki_text.rfind('</p>')+4]

        task.news['shingle_text'] = genshingle(ki_text,10) #создаем шинглы текста
        task.news['shingle_title'] = genshingle(task.news['title'],2) #создаем шинглы тайтла

        ki_text = pur.feed(ki_text) #очищаем от html тегов
        task.news['text'] = clean_text(ki_text,'normal') #очищаем от юникод сиволов и пустых абзацев
        task.news['text'] = task.news['text'].strip().replace("'","")
        ki_img_anons_text = grab.doc.select('//div[@class="daGallery"][1]/div[@class="newsImage"]/div') # подпись к фото, загоняем в подвал к копирайту
        if ki_img_anons_text:
            task.news['text'] = task.news['text'] + '<p style="text-align:right;">' + ki_img_anons_text.text() +'</p>'
        task.news['text'] = copyright(task.news['text'], 'komiinform')

        #скачивание картинки анонса
        task.news['img_anons'] = '' #обнуление объекта словаря
        link_anons_img = task.news['link_anons_img'] #обнуление переменной для записи ссылки на картинку-анонс
        
        if link_anons_img:
            path_to_img_folder = create_img_folder(task.news['date'])
            img_name = md5(link_anons_img.split("/")[-1].encode('utf-8')).hexdigest()[:15] + '.' + link_anons_img.split(".")[-1].lower()    #преобразуем имя файла картинки в хеш
            download_link_img_anons = path_to_img_folder + '/' + img_name
            #сохраняем в нужном формате cms instant
            img_anons_links.append(download_link_img_anons) #добавляем ссылку для проверки на 
           
            task.news['img_anons'] = download_link_img_anons[download_link_img_anons.find('media/')+6:]

            if not os.path.exists(download_link_img_anons):
                #передаем в очередь путь к папке и имя файла сгенерированное
                yield Task('image', url=link_anons_img, priority=task.priority, path=download_link_img_anons)

        #скачивание картинок из тела статьи
        mayby_img = grab.doc.select('//div[@class="daGallery"][2]//img')
        img_text = []
        for elem in mayby_img:
            if elem.attr('src'):
                if elem.attr('src').count('loginza') == 0 and elem.attr('src').count('_sm') == 0:
                    path_to_img_folder = create_img_folder(task.news['date'])
                    img_name = md5(elem.attr('src').split("/")[-1].encode('utf-8')).hexdigest()[:15] + '.' + elem.attr('src').split(".")[-1].lower()
                    new_link_to_img = path_to_img_folder + '/' + img_name
                    img_text.append(elem.attr('src') + ' ' + new_link_to_img)
                    if not os.path.exists(new_link_to_img):
                        yield Task('image', url=elem.attr('src'), priority=task.priority, path=new_link_to_img)

        #заменяем в тексте старые ссылки на картинки на новые-сгенерированные
        if img_text:
            for img in img_text:
                link_images = img.split(' ')
                task.news['text'] = task.news['text'].replace(link_images[0],'/media/' + link_images[1][link_images[1].find('media/')+6:])
        
        task.news['id_source'] = 1 #id источника парсинга - в данному случае комиинформ
        write_news_to_db(task.news) #Запись в базу



    def task_image(self, grab, task):
        grab.response.save(task.path)
        if img_anons_links.count(task.path) != 0:
            img_anons_links.remove(task.path) 

def main():
    bot = KomiinformSpider(thread_number=1)
    bot.run()

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()


'''
Алгоритм парсинга комиинформа (задачи)

1. Скриптинг:
- загрузка скрипта 1 раз в час

2. Подготовка
- загрузка в список 10-20 последних ссылок спарсенных статей с этого сайта

3. Обработка главной страницы
+ открываем главную страницу 
+ считываем ссылку на следующую страницу
+ считываем ссылки на новости, рубрику новости, текст анонса
+ проверка на наличие новости в базе - по заранее подготовленному списку
+ проверка на нужность по стоп листу категорий
+ запись ссылки, рубрики, анонса в словарь для записи в бд
+ создание задания на обработку страницы новости
   
4. Обработка страницы новости
- проверка текста на плагиат перед скачиванием всего остального? - сравнение со всеми новостями за последние 7 дней
    + создание шингла тайтла
    + очистка текста статьи
    + создание шингла текста статьи
    - проверка на плагиат (высчитать процент сходства на тестовой неделе комиинформа и бнкоми)         проверка контента - длиной 10 шинглов
        проверка заголовка с длиной 2 шингла
    - если плагиат дальше не обрабатывать статью

+ считываем нужные данные:
    + заголовок (юникод)
    + дату (приведение в порядок)
    + текст (очистка, юникод, копирайт)
    - ключевые слова
    - description
    - keywords
+ картинки
+ картинка-анонса
    + создание папки (год-месяц-день)
    + генерация имени файла
    + скачивание в нее картинки с новым именем (генерация задания)
    + запись в словарь ссылки на новое место расположение
    - подготовка переменной к типу как в бд
+ картинки в тексте
    + создание папки (год-месяц-день)
    + генерация имени файлов
    + скачивание в папку картинок с новым именем (генерация задания)
    + запись в временный список старой ссылки и новой
    + замена в тексте старой ссылки на новую
        
+ запись полученных данных в базу - простановка ключа - не проверено (одобрено)
? нужен ли ключ не проверно

- функция выгрузки в формат передачи данных
    ставить галку что статья выгружена
    категория статьи
        поставить нужную id (создать предварительно словарь)
    преобразование даты (либо сразу в парсинге)
'''