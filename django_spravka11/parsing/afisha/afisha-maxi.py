#кинотеатр кронверк синема макси
from grab import Grab
from purifier.purifier import HTMLPurifier
import datetime
import sys
sys.path
sys.path.append('/home/spravka/projects/spravka11/spravka11/parsing/')

from parsingfunct import clean_text, write_event_to_db, last_date_event

pur = HTMLPurifier({}) #удаляем все теги

def main():
    print('\n-- Парсинг афиши Кронверк синема Макси -  ' + str(datetime.datetime.now()))
    maxi = Grab(timeout=20, connect_timeout=20)

    date_now = datetime.date.today()

    exist_date_event = last_date_event('maxi', date_now.strftime("%Y-%m-%d")) #выгружаем последни даты из базы

    for i in range(3): #перебираем даты - 6 дней, больше на киноходе нет
        event = {}
        delta = datetime.timedelta(days=i)
        next_date = (date_now + delta)

        if exist_date_event.count(next_date.strftime("%Y-%m-%d")):
            print(next_date.strftime("%Y-%m-%d") + ' уже есть')
        else:
            next_link = 'http://kinohod.ru/syktyvkar/cinema/508/?date=' + next_date.strftime("%Y-%m-%d") #формируем ссылку
            
            maxi.go(next_link)
     
            count = maxi.doc.select('//div[@class="mblock"]')
            for x in range(len(count)):
                name = maxi.doc.select('//div[@class="mblock"][' + str(x+1) + ']//h1[@class="lnk"]')
                countli = maxi.doc.select('//div[@class="mblock"][' + str(x+1) + ']//ul/li')
                for i in range(len(countli)):
                    times = maxi.doc.select('//div[@class="mblock"][' + str(x+1) + ']//ul/li[' + str(i+1) + ']//h1')
                    type_films = maxi.doc.select('//div[@class="mblock"][' + str(x+1) + ']//ul/li[' + str(i+1) + ']//div[@class="first"]')
                    price_films = maxi.doc.select('//div[@class="mblock"][' + str(x+1) + ']//ul/li[' + str(i+1) + ']//div[@class="second"]')
                    
                    if not type_films.text():
                        type_films = '(NULL)'
                    else:
                        type_films = type_films.text().strip()
                    
                    price_films = int(price_films.text().replace('р.','').strip())

                    event = {
                        'name': name.text(),
                        'date': next_date.strftime("%Y-%m-%d"),
                        'time': times.text(),
                        'type_event': 'film',
                        'type_film': type_films,
                        'price': price_films,
                        'source_id': 2, #кронверк синема макси
                        'description': '',
                        'poster': ''
                    }
                    print(next_link)
                    write_event_to_db(event)

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()