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
from parsingfunct import create_img_folder, clean_text, last_core_event_links, write_core_event_to_db
import datetime
import urllib.parse

event ={}
date_now = datetime.date.today()
exist_news_links = last_core_event_links()

class KaroSpider(Spider):
    initial_urls = ['http://karofilm.ru']
    base_url = 'http://karofilm.ru'

    def create_grab_instance(self, **kwargs):
        grab = super(KaroSpider, self).create_grab_instance(**kwargs)
        grab.setup(timeout=20, connect_timeout=20)
        return grab

    def task_initial(self, grab, task):
        print('\n-- Парсинг информации о фильмах -  ' + str(datetime.datetime.now()))
        links = grab.doc.select('//td/a[@class="afisha-expand afisha-btn"]')
        prior = 0
        
        for link in links:
            if exist_news_links.count('http://karofilm.ru' + link.attr('href')):   #проверяем на уже спарсенные статьи
                print('Есть такая буква!')
            else:
                prior+=1
                yield Task('page', url=link.attr('href'), event=event, priority=prior)

    def task_page(self, grab, task):
        title = grab.doc.select('//h3')
        ganre = grab.doc.select('//p[@class="fp_header-genre"]')
        try:
            limit = grab.doc.select('//h3/span[@class="fp_header-age"]').text()
        except:
            limit = ''

        title = title.text().replace(limit,'')
        poster = grab.doc.select('//div[@class="col-sm-6 film_page-poster-big hidden-xs"]/img')

        info = grab.doc.select('//div[@class="film_page-film-data col-sm-6 col-xs-12"]/p')
        try:
            descr = grab.doc.select('//div[@class="film_page-film-data col-sm-6 col-xs-12"]/div[2]/p').text()
        except:
            descr = grab.doc.select('//div[@class="film_page-film-data col-sm-6 col-xs-12"]/div[1]/p').text()
        #images = grab.doc.select('//div[@class="fp-shots-grid"]/a')

        description = ''
        for i in info:
            description += i.text().replace("'"," ") + '\n'   
        description += clean_text(descr.replace("'"," "), 'normal')

        if poster.attr('src'):
            path_to_img_folder = create_img_folder(date=date_now.strftime("%Y-%m-%d"), type='event')
            img_name = md5(poster.attr('src').split("/")[-1].encode('utf-8')).hexdigest()[:15] + '.' + poster.attr('src').split(".")[-1].lower()
            new_link_to_img = path_to_img_folder + '/' + img_name
            if not os.path.exists(new_link_to_img):
                fix_link = urllib.parse.quote(poster.attr('src'))
                yield Task('image', url=fix_link, priority=task.priority, path=path_to_img_folder, name_img=img_name)
            poster = new_link_to_img[new_link_to_img.find('/media/')+7:]

        
        '''
        imgs = []
        for im in images:
            if im.attr('href'):
                path_to_img_folder = create_img_folder(date_now.strftime("%Y-%m-%d"))
                img_name = md5(im.attr('href').split("/")[-1].encode('utf-8')).hexdigest()[:15] + '.' + im.attr('href').split(".")[-1].lower()
                new_link_to_img = path_to_img_folder + '//' + img_name
                if not os.path.exists(new_link_to_img):
                    fix_link = urllib.parse.quote(im.attr('href'))
                    yield Task('image', url=fix_link, priority=task.priority, path=path_to_img_folder, name_img=img_name)
                    imgs.append(new_link_to_img)

        for img in imgs:
            description += img
        '''

        event = {
            'title': title.replace("'", ''),
            'description': description,
            'event_type': 1,
            'ganre': ganre.text().replace(' .', ','),
            'limit_year': limit,
            'poster': poster,            
            'url': task.url
        }
        write_core_event_to_db(event)

    def task_image(self, grab, task):
        grab.response.save(task.path + '/%s' % task.name_img)

def main():
    bot = KaroSpider(thread_number=1)
    bot.run()

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()