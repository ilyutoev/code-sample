import datetime
from parsingfunct import clean_text, write_event_to_db, last_date_event
import os

#открываем файл, построчно вытаскиваем ячейки в переменные, разбиваем дату и готовим словарь
def unpack_line(line):
    line_list = line.split(";")
    file_name = line_list[0]
    file_type = line_list[1]
    file_date = line_list[2]
    file_time = line_list[3]
    file_price = line_list[4]
    return file_name, file_type, file_date, file_time, file_price

def main():
    filename = 'raduga.csv'
    f = open(filename, "r", encoding="cp1251")
    lines = f.readlines()

    for line in lines:
        if not line.find("#") > -1:
            # извлекаем данные из строки
            file_name, file_type, file_date, file_time, file_price = unpack_line(line)
            
            #определяем дату начала показа и разницу между началом и концом
            startdate = file_date.split('-')[0].strip().split('.')
            enddate = file_date.split('-')[1].strip().split('.')
            count_day = int(enddate[0]) - int(startdate[0])
            startdate = datetime.date(int(startdate[2]),int(startdate[1]),int(startdate[0]))
            exist_date_event = last_date_event('raduga', startdate.strftime("%Y-%m-%d")) #выгружаем последни даты из базы

            for day in range(count_day+1):
                event = {}
                delta = datetime.timedelta(days=day)
                next_date = (startdate + delta)

                if exist_date_event.count(next_date.strftime("%Y-%m-%d")):
                    print(next_date.strftime("%Y-%m-%d") + ' уже есть')
                else:
                    if file_type == '':
                        file_type = '2D'

                    event = {
                        'name': file_name,
                        'date': next_date.strftime("%Y-%m-%d"),
                        'time': file_time,
                        'type_event': 'film',
                        'type_film': file_type,
                        'price': int(file_price),
                        'source_id': 4 #радуга
                    }

                    write_event_to_db(event)

    f.close()
    os.remove(filename)    #удаляем файлик

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()