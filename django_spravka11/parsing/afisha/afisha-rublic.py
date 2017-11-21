from grab import Grab
from purifier.purifier import HTMLPurifier
import datetime
import sys
sys.path
sys.path.append('/home/spravka/projects/spravka11/spravka11/parsing/')
from parsingfunct import clean_text, write_event_to_db, last_date_event

pur = HTMLPurifier({}) #удаляем все теги

def main():
    print('\n-- Парсинг афиши Рублика -  ' + str(datetime.datetime.now()))
    rub = Grab(timeout=20, connect_timeout=20)

    date_now = datetime.date.today()
    
    exist_date_event = last_date_event('rublic', date_now.strftime("%Y-%m-%d")) #выгружаем последни даты из базы
        
    for i in range(14): #перебираем даты
        event = {}
        delta = datetime.timedelta(days=i)
        next_date = (date_now + delta)

        if exist_date_event.count(next_date.strftime("%Y-%m-%d")):
            print(next_date.strftime("%Y-%m-%d") + ' уже есть')
        else:
            #http://rubliongroup.ru/include/schedule.php?AJAX_SCHEDULE=Y&SES=06-05-2015&THEATRE_ID=5345
            next_link = 'http://rubliongroup.ru/include/schedule.php?AJAX_SCHEDULE=Y&SES=' + next_date.strftime("%m-%d-%Y") + '&THEATRE_ID=5345'#формируем ссылку
            
            rub.go(next_link)
            allpage = rub.doc.select('//div').html()
            allpage = pur.feed(clean_text(allpage, 'normal'))

            if allpage.find('Расписание готовится') == -1:
                names = rub.doc.select('//table//table//tr/td[@class="name"]')
                times = rub.doc.select('//table//table//tr/td[@class="time"]')
                prices = rub.doc.select('//table//table//tr/td[@class="price"]')

                for time, name, price in zip(times, names, prices):
                    type_film = None
                    if name.text().find('3D') != -1:
                        type_film = '3D'
                    name = name.text()[:name.text().find('(')].strip()
                    price = clean_text(price.text(),'normal').replace('/','').strip()

                    event = {
                        'name': name,
                        'date': next_date.strftime("%Y-%m-%d"),
                        'time': time.text(),
                        'type_event': 'film',
                        'type_film': str(type_film),
                        'price': price,
                        'source_id': 1, #рублик
                        'description': '',
                        'poster': ''
                    }
                    print(next_link)
                    write_event_to_db(event)

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()