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
from parsingfunct import create_img_folder, clean_text, last_date_event, write_event_to_db
import datetime
import urllib.parse


#сайт кривенький - надо руками перепрверять как что добавилось - часто даты в описание забиты
event ={}
exist_date_event = last_date_event('filarmonia', '2015-01-01') #указана фиксированная дата
month_list = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}

class FilarmoniaSpider(Spider):
    initial_urls = ['http://filarmoniakomi.ru/afisha/']
    base_url = 'http://filarmoniakomi.ru/afisha'

    def create_grab_instance(self, **kwargs):
        grab = super(FilarmoniaSpider, self).create_grab_instance(**kwargs)
        grab.setup(timeout=20, connect_timeout=20)
        return grab

    def task_initial(self, grab, task):
        next_links = grab.doc.select('//div[@class="months"]/a')
        prior = 0
        print('\n-- Парсинг афиши Филармонии -  ' + str(datetime.datetime.now()))
        
        for link in next_links:
            prior+=1
            yield Task('page', url=link.attr('href'), event=event, priority=prior)

    def task_page(self, grab, task):
        print(task.url)
        #task.event['title']
        titles = grab.doc.select('//ul[@id="afisha"]/li/p/span[@class="title"]')
        dates_event = grab.doc.select('//ul[@id="afisha"]/li/p/span[@class="date"]')
        images = grab.doc.select('//ul[@id="afisha"]/li/img')
        contents = grab.doc.select('//ul[@id="afisha"]/li/a')

        for title, date_event, img, content in zip(titles, dates_event, images, contents):
            title = clean_text(title.text(), 'normal')

            try:
                month_test = clean_text(date_event.text(), 'normal').split(' ')[1]
                month_test = month_list[month_test]
            except:
                month_test = False

            date = clean_text(date_event.text(), 'normal')[:-6]
            time = clean_text(date_event.text(), 'normal')[-5:].replace('.', ':')
            content = clean_text(content.text(), 'normal')

            year = task.url.split('/')[-3]
            date = date.split(' ')[0].split('-')

            try:
                int(date[0])
                integ = True
            except:
                integ = False

            if integ and month_test:
                startdata = datetime.date(int(year),int(month_test),int(date[0]))

                if img.attr('src'):
                    path_to_img_folder = create_img_folder(date=startdata.strftime("%Y-%m-%d"), type='event')
                    img_name = md5(img.attr('src').split("/")[-1].encode('utf-8')).hexdigest()[:15] + '.' + img.attr('src').split(".")[-1].lower()
                    new_link_to_img = path_to_img_folder + '/' + img_name
                    if not os.path.exists(new_link_to_img):
                        fix_link = urllib.parse.quote(img.attr('src'))
                        yield Task('image', url=fix_link, priority=task.priority, path=path_to_img_folder, name_img=img_name)
                if exist_date_event.count(startdata.strftime("%Y-%m-%d")):
                    print(startdata.strftime("%Y-%m-%d") + ' уже есть')
                else:
                    if len(date) == 2:
                        for i in range(int(date[1]) - int(date[0]) + 1):
                            startdata = datetime.date(int(year),int(month_test),int(date[0]) + i)
                            event = {
                                'name': title,
                                'date': startdata.strftime("%Y-%m-%d"),
                                'time': time,
                                'type_event': 'koncert',
                                'type_film': '',
                                'price': 0,
                                'source_id': 7, #филармония
                                'description': content,
                                'poster': new_link_to_img[new_link_to_img.find('/media/')+7:]
                            }
                            write_event_to_db(event)


                    else:
                        startdata = datetime.date(int(year),int(month_test),int(date[0]))
                        event = {
                            'name': title,
                            'date': startdata.strftime("%Y-%m-%d"),
                            'time': time,
                            'type_event': 'koncert',
                            'type_film': '',
                            'price': 0,
                            'source_id': 7, #филармония
                            'description': content,
                            'poster': new_link_to_img[new_link_to_img.find('/media/')+7:]
                        }
                        write_event_to_db(event)

    def task_image(self, grab, task):
        grab.response.save(task.path + '/%s' % task.name_img)

def main():
    bot = FilarmoniaSpider(thread_number=1)
    bot.run()

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()