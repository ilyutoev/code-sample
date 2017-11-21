from grab import Grab
from purifier.purifier import HTMLPurifier
import sys
sys.path
sys.path.append('/home/spravka/projects/spravka11/spravka11/parsing/')
from parsingfunct import clean_text, write_event_to_db, last_date_event
from datetime import datetime, date

def main():
    print('\n-- Парсинг афиши Драмтеатра -  ' + str(datetime.now()))

    month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}

    drama = Grab(timeout=20, connect_timeout=20)
    drama.go('http://quicktickets.ru/teatr-dramy-viktora-savina')

    titles = drama.doc.select('//div[@id="events-list"]//div[@class="item"]//div[@class="c"]/h3')
    descriptions = drama.doc.select('//div[@id="events-list"]//div[@class="item"]//div[@class="c"]/div[@class="d"]')
    seanses = drama.doc.select('//div[@id="events-list"]//div[@class="item"]//div[@class="c"]/div[@class="row sessions sessions-near"]')
    
    now_month = date.today().month
    now_year = date.today().year
    next_year = now_year + 1

    #вычисляем первую дату для выборки из базы - проверка на уже загруженные даты 
    start_date = drama.doc.select('//div[@id="events-list"]//div[@class="item"]//div[@class="c"]/div[@class="row sessions sessions-near"]//a').text()
    start_date = start_date.replace(',','').split(' ')
    if now_month in (10,11,12) and int(month[start_date[1]]) in (1,2):
        start_date = date(next_year, int(month[start_date[1]]), int(start_date[0]))
    else:
        start_date = date(now_year, int(month[start_date[1]]), int(start_date[0]))
    exist_date_event = last_date_event('dramakomi', start_date)

    #отрабатываем события
    for title, desc, seans in zip(titles, descriptions, seanses):
        for date_time in seans.select('.//a'):
            date_time = date_time.text().replace(',','').split(' ')
            time = date_time[2]
            if now_month in (10,11,12) and int(month[date_time[1]]) in (1,2):
                date_time = date(next_year, int(month[date_time[1]]), int(date_time[0]))
            else:
                date_time = date(now_year, int(month[date_time[1]]), int(date_time[0]))

            if exist_date_event.count(date_time.strftime("%Y-%m-%d")):
                print(date_time.strftime("%Y-%m-%d") + ' уже есть')
            else:
                event = {
                    'name': title.text(),
                    'date': date_time.strftime("%Y-%m-%d"),
                    'time': time,
                    'type_event': 'teatr',
                    'type_film': '',
                    'price': 0,
                    'source_id': 5, #драмтеатр
                    'description': desc.text(),
                    'poster': ''
                }

                write_event_to_db(event)

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()