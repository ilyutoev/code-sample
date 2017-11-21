from grab import Grab
from purifier.purifier import HTMLPurifier
import sys
sys.path
sys.path.append('/home/spravka/projects/spravka11/spravka11/parsing/')
from parsingfunct import clean_text, write_event_to_db, last_date_event, data_change
import datetime

pur = HTMLPurifier({
    'p': [''], # разрешает все атрибуты у тега div
    'br': [''],
    'b': [''],
    # все остальные теги удаляются, но их содержимое остается
})


#Комиоперу парсить с двух мест - http://quicktickets.ru/teatropery и с основного сайта (брать цену)

def main():
    print('\n-- Парсинг афиши Тетра оперы и балета -  ' + str(datetime.datetime.now()))
    opera = Grab(document_charset='utf-8', timeout=20, connect_timeout=20)
    opera.go('http://komiopera.ru/index.php?option=com_content&view=article&id=95&Itemid=134')
    #opera.response.body = clean_text(opera.response.body, 'normal')

    dates = opera.doc.select('//table//table//tr/td[1]/div/b')
    titles = opera.doc.select('//table//table//tr/td[2]/div/b')
    contents1 = opera.doc.select('//table//table//tr/td[2]/div/i')
    contents2 = opera.doc.select('//table//table//tr/td[3]/div/b')
    times = opera.doc.select('//table//table//tr/td[3]/div')

    date_for_db = data_change(dates[0].text(), 'komiopera')    
    exist_date_event = last_date_event('komiopera', date_for_db)
    for date, title, content1, content2, time in zip(dates, titles,contents1, contents2, times):
        if exist_date_event.count(data_change(date.text(), 'komiopera')):
            print(data_change(date.text(), 'komiopera') + ' уже есть')
        else:
            event = {
                'name': title.text().strip(),
                'date': data_change(date.text(), 'komiopera'),
                'time': time.text()[-5:],
                'type_event': 'teatr',
                'type_film': '',
                'price': 0,
                'source_id': 6, #коми опера
                'description': content1.text().strip() + ', ' + content2.text().strip(),
                'poster': ''
            }
            write_event_to_db(event)

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()