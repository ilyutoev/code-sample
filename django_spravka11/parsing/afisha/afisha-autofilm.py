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
    filename = 'autofilm.csv'
    f = open(filename, "r", encoding="cp1251")
    lines = f.readlines()

    for i, line in enumerate(lines):
        if not line.find("#") > -1:
            # извлекаем данные из строки
            file_name, file_type, file_date, file_time, file_price = unpack_line(line)
            
            #определяем дату начала показа и разницу между началом и концом
            date = file_date.strip().split('.')
            date = datetime.date(int(date[2]),int(date[1]),int(date[0]))
            
            if i == 1: #функцию вызываем только один раз
                exist_date_event = last_date_event('autofilm', date.strftime("%Y-%m-%d")) #выгружаем последни даты из базы
            
            event = {}
            if exist_date_event.count(date.strftime("%Y-%m-%d")):
                print(date.strftime("%Y-%m-%d") + ' уже есть')
            else:
                if file_type == '':
                    file_type = '2D'

                event = {
                    'name': file_name,
                    'date': date.strftime("%Y-%m-%d"),
                    'time': file_time,
                    'type_event': 'film',
                    'type_film': file_type,
                    'price': int(file_price),
                    'source_id': 6 #автокинотеа
                }

                write_event_to_db(event)
    f.close()
    os.remove(filename)    #удаляем файлик

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    main()