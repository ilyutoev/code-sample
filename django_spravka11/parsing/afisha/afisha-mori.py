#Кинотеатр MORI CINEMA Сыктывкар
from grab import Grab
from purifier.purifier import HTMLPurifier
import datetime
import sys
sys.path
sys.path.append('/home/spravka/projects/spravka11/spravka11/parsing/')
from parsingfunct import clean_text, write_event_to_db, last_date_event

pur = HTMLPurifier({}) #удаляем все теги

def main():
    print('\n-- Парсинг афиши Мори синема - Июнь -  ' + str(datetime.datetime.now()))
    mori = Grab(timeout=20, connect_timeout=20)
    ticket = Grab(timeout=20, connect_timeout=20)

    #берем данные только с дней с точной датой, либо корректируемся под проверку - какой день - его за основу и вперед

    date_now = datetime.date.today()
    exist_date_event = last_date_event('mori', date_now.strftime("%Y-%m-%d")) #выгружаем последни даты из базы

    mori.go('http://www.mori-cinema.ru/cinema_detail/4768_syktyvkar/')

    #ебучие верстальщики сайта сломали дом дерево - приходится изъебываться
    mori.response.body = mori.response.body.replace(b'</div> */ --!>',b'*/ --></div>')
    
    count_day = mori.doc.select('//div[@class="dDatas width"]/div[@class="tbl_timetable hidden"]//table') #считаем количесво вкладок с сеансами, вкладка - день, начинаем со второй вкладки, либо с раннего утра сегодняшней влкадки

    #проверяем, что даты верно указаны, начиная с третьей таблицы указана дата - с ней и сверяемся
    if (date_now + datetime.timedelta(days=2)).strftime("%d.%m.%Y") == mori.doc.select('//div[@class="dDatas width"]/div[@class="tbl_timetable hidden"]//table[1]//th').text():
        for day in range(len(count_day)):
            event = {}
            delta = datetime.timedelta(days=day+2)#дата на два дня вперед
            next_date = (date_now + delta)

            if exist_date_event.count(next_date.strftime("%Y-%m-%d")):
                print(next_date.strftime("%Y-%m-%d") + ' уже есть')
            else:
                #определяем количество фильмов в дне
                print('Текущая дата ' + str(next_date))
                count_films = mori.doc.select('//div[@class="dDatas width"]/div[@class="tbl_timetable hidden"]//table[' + str(day+1) + ']//tr')

                temp_name = ''
                for film in range(len(count_films)-2):
                    #проврка на пустые строки без информации о фильмах
                    try:
                        mori.doc.select('//div[@class="dDatas width"]/div[@class="tbl_timetable hidden"]//table[' + str(day+1) + ']//tr[' + str(film+3) + ']/td').text()
                        next = True
                    except:
                        next = False

                    if next:
                        name = mori.doc.select('//div[@class="dDatas width"]/div[@class="tbl_timetable hidden"]//table[' + str(day+1) + ']//tr[' + str(film+3) + ']/td[@rowspan]')

                        #проверка на фильмы с двойными стркоами. у фильма два вида - 2д и 3д, во второй строке нет названия
                        correct = 0
                        try:
                            rowattr = name.attr('rowspan')
                            name = name.text()
                            if rowattr == '2':
                                temp_name = name
                        except:
                            rowattr = '77'
                            correct = 1
                            name = temp_name

                        print(name)
                        
                        type_film = mori.doc.select('//div[@class="dDatas width"]/div[@class="tbl_timetable hidden"]//table[' + str(day+1) + ']//tr[' + str(film+3) + ']/td['+  str(2-correct) + ']')

                        times = mori.doc.select('//div[@class="dDatas width"]/div[@class="tbl_timetable hidden"]//table[' + str(day+1) + ']//tr[' + str(film+3) + ']/td['+  str(3-correct) + ']/a')

                        for time in times:
                        #вычленяем из ссылки атрибут для передачи в кассу рамблера для поиска ценника
                            argument = time.attr('href')[time.attr('href').rfind(',')+1:time.attr('href').rfind(');')]
                            #делаем запрос к кассе и узнаем цену на конкретный сеанс
                            ticket.go('https://widget.kassa.rambler.ru/place/hallplanajax/xxxxxxxxxx?widgetid=19484&clusterradius=61'.replace('xxxxxxxxxx',argument))
                            check = ticket.doc.select('//div').text()
                            if check.count('нельзя') > 0:
                                price = 0
                            else:
                                price = ticket.doc.select('//ul[@class="seats-icon-details"]/li[1]/span').text()
                                price = int(price[price.rfind('(')+1:price.rfind('руб')-1])
                            
                            event = {
                                'name': name,
                                'date': next_date.strftime("%Y-%m-%d"),
                                'time': time.text(),
                                'type_event': 'film',
                                'type_film': type_film.text(),
                                'price': price,
                                'source_id': 3, #Кинотеатр MORI CINEMA Сыктывкар
                                'description': '',
                                'poster': ''
                            }
                            write_event_to_db(event)
                    

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()