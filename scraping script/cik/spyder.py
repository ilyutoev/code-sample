import logging
from grab.spider import Spider, Task
from grab import Grab
import re
import pymysql
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, create_engine, BigInteger
from sqlalchemy.orm import sessionmaker
import random
import json
from  sqlalchemy.exc import IntegrityError

class ExampleSpider(Spider):

    def prepare(self):
        self.counter = 1
        
        self.starturl = 'http://cikrf.ru/services/lk_tree/?first=1&id=%23'
        self.urlpattern_json = 'http://cikrf.ru/services/lk_tree/?id='
        self.urlpattern_page = 'http://cikrf.ru/services/lk_address/'

    def task_generator(self):
        #yield Task('jsonresponse', url=self.starturl)

        yield Task('jsonresponse', url='http://cikrf.ru/services/lk_tree/?id=5410716641', region='Республика Дагестан')
        

    def task_jsonresponse(self, grab, task):

        try:
            response = json.loads(str(grab.doc.body).replace("b'","").replace("'", "").replace('\\',''))
        except:
            response = None
            self.add_task(Task('jsonresponse', url=task.url, delay=1, region=task.region))
            print('----- Ответ не похож на json -----', task.url)

        if response:
            if task.url == self.starturl:
                response = response[0]['children']
            for resp in response:
                temp_id = resp['id']
                temp_intid = resp['a_attr']['intid']
                temp_levelid = resp['a_attr']['levelid']

                if temp_levelid == '8':
                    g = Grab(url=self.urlpattern_page + temp_intid + '?do=result', document_charset='windows-1251')
                    yield Task('pageresponse', grab=g, urlid=temp_id, region=task.region)
                elif temp_levelid == '11':
                    pass
                else:
                    yield Task('jsonresponse', url=self.urlpattern_json + temp_id, region=task.region)
                    print(self.counter, 'Отправлена в работу ссылка', temp_id, 'уровень', temp_levelid)
                    self.counter += 1

        else:
            print('----- Похоже пустой json -----', task.url)

    def task_pageresponse(self, grab, task):

        try:
            text = grab.doc.select('//div[@class="dotted"]').text()
        except:
            print('    На странице нет текста, отправляем ссылку заново в очередь')
            self.add_task(Task('pageresponse', url=task.url, delay=1, region=task.region))
            text = None

        if text:
            if 'что данные об избирательном участке по введенному Вами адресу места' in text:
                print('----- На странице нет информации об участковой комиссии -----', task.urlid)

            elif 'Участковая избирательная комиссия' in text:
                try:
                    temp_uik = grab.doc.select('//p[contains(text(), "избирательная комиссия")]').text().replace('№','').split(' ')[-1]
                    try:
                        temp_phone = grab.doc.select('//p[contains(text(), "телефон")]').text().replace('телефон:','').strip()
                    except:
                        temp_phone = ''
                    try:
                        temp_address = temp_uik + ' NNN ' + grab.doc.select('//p[contains(text(), "Адрес:")]').text().replace('Адрес:','').replace('Адрес УИК и помещения для голосования:', '').strip()
                    except:
                        temp_address = temp_uik
                        print('!!!!!! С адресом косяк !!!!!!!!', task.url)
                    temp_region = task.region

                    session = Session()
                    temp = Uikrf(region = temp_region, uik = temp_uik, address = temp_address, phone = temp_phone, pageurl=task.url) 
                    session.add(temp)
                    session.commit()
                    session.close()
                    print('Добавлена информация о УИК', task.url)
                except IntegrityError:
                    session.close()
                    print('!! Не удалось добавить в базу даннах - поле повторяется', task.url)
                
            else:
                print('----- Странная страница - не УИК -----', task.urlid, task.url, )


    def task_jsonresponse_fallback(self, task):
        print('--- Что-то несрослось jsonresponse! ---', task.url)
        #self.add_task(Task('page', url=task.url, delay=5, id=task.id, domen=task.domen))


    def task_pageresponse_fallback(self, task):
        print('--- Что-то несрослось pageresponse! ---', task.url)
        #self.add_task(Task('page', url=task.url, delay=5, id=task.id, domen=task.domen))


if __name__ == '__main__':

    #настройка базы данных
    engine = create_engine("mysql+pymysql://root:@localhost/medico?charset=utf8", encoding='utf8', echo=False)

    #engine = create_engine("mysql+pymysql://root:root@localhost/adv?charset=utf8", encoding='utf8', echo=False)

    Base = declarative_base()
    class Uikrf(Base):
        __tablename__ = 'uik2'

        id = Column(Integer, primary_key=True)
        region = Column(String(255))
        uik = Column(Integer)
        address = Column(String(255), unique=True)
        phone = Column(String(255))
        checked = Column(Integer)
        pageurl = Column(String(255))

        def __repr__(self):
            return "<Uikrf(id='%s', uik='%s')>" % (self.id, self.uik)

    Base.metadata.create_all(engine) 
    Session = sessionmaker(bind=engine)
    session = Session()

    #logging.basicConfig(level=logging.DEBUG)
    
    bot = ExampleSpider(thread_number=15)
    #bot.load_proxylist('proxy.txt', 'text_file')
    bot.run()