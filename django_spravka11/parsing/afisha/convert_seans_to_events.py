import pymysql
import json
from datetime import datetime

'''
    по этому списку делаем замену через функцию корректировки (возможно преобразовать ее на работу из файла или из списка)
'''

def check_db_seans():
    "Функция ищет названия мероприятий в таблице сеансов, не имеющих соответствия в таблице мероприятий - т.е. эти сеансы не будут показаны пользователю"
    def different_and_correct_names_from_db():
        db = pymysql.connect(host="localhost", user="spravuser", passwd="12spr23FFd33", db="spravka11", charset="utf8")

        cursor = db.cursor()
        #запрос к таблице с сеансами и выборка всех названий
        sql = """SELECT name FROM pars_afisha where type_event = 'film' and event_id IS NULL"""
        cursor.execute(sql)
        data = cursor.fetchall()

        names_from_seans = set(data)

        #запрос к таблице с мероприятиями (корневыми) и выборка всех названий
        sql = """SELECT title FROM events_events WHERE event_type_id = 1"""
        cursor.execute(sql)
        data = cursor.fetchall()

        names_from_events = set(data)

        #поиск отличий между множествами
        different = names_from_seans.difference(names_from_events)

        return different, names_from_events

    # вспомогательная функция автокоррекции названий событий (используется дл фильмов) 
    def auto_correct_db_season(different, correct_names):
        '''На входе множество с различиями и корректное множество с названиями
        На выходе двумерный список неверное название - верное название'''

        def canonize(source): #функция канонизации текста
            source = source.lower()
            stop_symbols = '. ,;:!?-'
            
            for char in stop_symbols:
                source = source.replace(char, '')
            
            return source
        
        def canonize_list(name_list):
            temp_list = []
            for i, name in enumerate(name_list):
                temp_list.append([])
                temp_list[i].append(name)
                temp_list[i].append(canonize(name))
            return temp_list

        different_canonize = canonize_list(different)
        correct_names_canonize = canonize_list(correct_names)

        wrong_correct_list = []
        i = 0
        for diff in different_canonize:
            for correct in correct_names_canonize:
                if diff[1] == correct[1]:
                    wrong_correct_list.append([])
                    wrong_correct_list[i].append(diff[0])
                    wrong_correct_list[i].append(correct[0])
                    i += 1
        
        return wrong_correct_list


    #ищем различия между таблицами по полю название мероприятия
    different, names_from_events = different_and_correct_names_from_db()

    #делаем автокоррекцию названий
    different_to_autocorrect = list(x[0] for x in different)
    correct_name_to_autocorrect = list(x[0] for x in names_from_events)

    wrong_correct_list = auto_correct_db_season(different_to_autocorrect, correct_name_to_autocorrect)

    correct_db_seans(wrong_correct_list=wrong_correct_list)

    #еще раз запускаем проверку различия между таблицами по полю название мероприятия
    different, names_from_events = different_and_correct_names_from_db()

    #Не найденные названия фильмов пишем в спеиальную базу для ручной коррекции
    db = pymysql.connect(host="localhost", user="spravuser", passwd="12spr23FFd33", db="spravka11", charset="utf8")
    cursor = db.cursor()

    for title in different:
        cursor = db.cursor()
        sql = """SELECT id FROM misc_wrongright WHERE wrong_title='{}';""".format(title[0])
        cursor.execute(sql)
        data = cursor.fetchall()
        if not data:
            sql = """INSERT INTO misc_wrongright (wrong_title) VALUES ('{wrong_title}')""".format(wrong_title=title[0])
            cursor.execute(sql)
            db.commit()
            if __name__ == '__main__':
                print('Запись в "верно-неверно" внесена - ' + title[0])

def correct_db_seans(correct_from_wrongright_db=False, wrong_correct_list=None):

    def correct_db(wrong_name, right_name):
        cursor = db.cursor()
        sql = """SELECT id FROM pars_afisha where name = '{}'""".format(wrong_name)
        cursor.execute(sql)
        data = cursor.fetchall()

        list_wrong_id = [i[0] for i in data]

        for i in list_wrong_id:
            sql = """UPDATE pars_afisha SET name = '{0}' WHERE id = {1}""".format(right_name, i)
            cursor.execute(sql)
            db.commit()

    db = pymysql.connect(host="localhost", user="spravuser", passwd="12spr23FFd33", db="spravka11", charset="utf8")

    if correct_from_wrongright_db:
        cursor = db.cursor()
        sql = """SELECT wrong_title, right_title FROM misc_wrongright where right_title IS NOT NULL"""
        cursor.execute(sql)
        data = cursor.fetchall()
        for line in data:
            correct_db(line[0], line[1])

    if wrong_correct_list:
        if __name__ == '__main__':
            print('я сработал')
        for line in wrong_correct_list:
            wrong_name = line[0]
            right_name = line[1]
            correct_db(wrong_name, right_name)

def seans_name_to_event_id():
    '''
    Функция проставляет в таблице сеансов event_id в соответствии с названеиями из таблицы мероприятий
    Функцию запускать на стороне сайта (когда у мероприятий есть верные id).
    '''

    db = pymysql.connect(host="localhost", user="spravuser", passwd="12spr23FFd33", db="spravka11", charset="utf8")

    cursor = db.cursor()
    #надо считывать только фильмы - сделать проверку where type_event == film
    #делаем выборку (название - id) из таблицы мероприятий
    sql = """SELECT title, id FROM events_events WHERE event_type_id = 1"""

    cursor.execute(sql)
    data = cursor.fetchall()
    events = dict(data)

    #пробегаем по полученному словарю
    for event in events:

        #делаем запрос из "сеансов" по названию мероприятия и выбираем их id
        sql = """SELECT id FROM pars_afisha WHERE name = '{}' AND event_id IS NULL""".format(event)
        cursor.execute(sql)
        data = cursor.fetchall()

        if data:
            for i in data:
                sql = """UPDATE pars_afisha SET event_id = {0} WHERE id = {1}""".format(events[event], i[0])
                cursor.execute(sql)
                db.commit()

#функция переноса спарсенных киносеансов в сеансы на сайте
def kino_seans_to_real_db():
    db = pymysql.connect(host="localhost", user="spravuser", passwd="12spr23FFd33", db="spravka11", charset="utf8")
    cursor = db.cursor()
    sql = """SELECT id, event_id, date, time, price, place FROM pars_afisha WHERE type_event = 'film' and (import IS NULL or import = 0) and event_id IS NOT NULL"""

    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        sql = """INSERT INTO events_session (date, time, price, event_id, place_id) VALUES ("{date}", '{time}', {price}, {event_id}, {place_id})""".format(date=d[2], time=d[3], price=d[4], event_id=d[1], place_id=d[5])
        cursor.execute(sql)
        db.commit()

        sql = """UPDATE pars_afisha SET import = 1 WHERE id = {0}""".format(d[0])
        cursor.execute(sql)
        db.commit()
        if __name__ == '__main__':
            print('Сеанс номер {0} перенесен и помечен как выгруженный'.format(d[0]))

#фукция переноса спарсеных остальных мероприятий (не кино) - в две основные таблиц - мероприятия и сеансы

#создаем мероприятия. выгружаем все названия из таблицы, в множество, проверяем на наличие в основной таблице, игнорим или добавляем запись.
def pars_event_to_db():
    type_ev = {'teatr': 2, 'sport': 4, 'koncert': 3}
    #выгружаем все названия из спарсенной таблицы
    db = pymysql.connect(host="localhost", user="spravuser", passwd="12spr23FFd33", db="spravka11", charset="utf8")
    cursor = db.cursor()
    sql = """SELECT id, name, description, type_event, poster FROM pars_afisha WHERE event_id IS NULL and type_event != 'film'"""
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        #проверяем, есть ли такое название в 
        sql = """SELECT id FROM events_events WHERE title = '{0}' and event_type_id = {1}""".format(d[1], type_ev[d[3]])
        cursor.execute(sql)
        datanew = cursor.fetchall()
        if datanew:
            if __name__ == '__main__':
                print('Мероприятие "{}" уже есть в базе'.format(d[1]))
        else:
            if d[4]:
                sql = """INSERT INTO events_events (title, description, event_type_id, poster) VALUES ('{title}', '{description}', {event_type_id}, '{poster}')""".format(title=d[1], description=d[2], event_type_id=type_ev[d[3]], poster=d[4])
            else:
                sql = """INSERT INTO events_events (title, description, event_type_id) VALUES ('{title}', '{description}', {event_type_id})""".format(title=d[1], description=d[2], event_type_id=type_ev[d[3]])
            cursor.execute(sql)
            db.commit()
            if __name__ == '__main__':
                print('Мероприятие "{}" добавлено в базу'.format(d[1]))

def event_set_event_id():
    db = pymysql.connect(host="localhost", user="spravuser", passwd="12spr23FFd33", db="spravka11", charset="utf8")

    cursor = db.cursor()
    #надо считывать только фильмы - сделать проверку where type_event == film
    #делаем выборку (название - id) из таблицы мероприятий
    sql = """SELECT title, id FROM events_events WHERE event_type_id IN (2,3,4)"""

    cursor.execute(sql)
    data = cursor.fetchall()
    events = dict(data)

    #пробегаем по полученному словарю
    for event in events:
        #делаем запрос из "сеансов" по названию мероприятия и выбираем их id
        sql = """SELECT id FROM pars_afisha WHERE name = '{}' AND event_id IS NULL""".format(event)
        cursor.execute(sql)
        data = cursor.fetchall()

        if data:
            for i in data:
                sql = """UPDATE pars_afisha SET event_id = {0} WHERE id = {1}""".format(events[event], i[0])
                cursor.execute(sql)
                db.commit()
    if __name__ == '__main__':
        print('id сеансам проставлены!')


def event_seans_to_real_db():
    db = pymysql.connect(host="localhost", user="spravuser", passwd="12spr23FFd33", db="spravka11", charset="utf8")
    cursor = db.cursor()
    sql = """SELECT id, event_id, date, time, price, place FROM pars_afisha WHERE type_event IN ('teatr', 'sport', 'koncert') and (import IS NULL or import = 0) and event_id IS NOT NULL"""

    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        #проверка на существование места с нужным id
        sql = """SELECT id FROM events_eventplace WHERE id = {0}""".format(d[5])
        cursor.execute(sql)
        datanew = cursor.fetchall()
        if datanew:
            sql = """INSERT INTO events_session (date, time, price, event_id, place_id) VALUES ("{date}", '{time}', {price}, {event_id}, {place_id})""".format(date=d[2], time=d[3], price=d[4], event_id=d[1], place_id=d[5])
            cursor.execute(sql)
            db.commit()

            sql = """UPDATE pars_afisha SET import = 1 WHERE id = {0}""".format(d[0])
            cursor.execute(sql)
            db.commit()
            if __name__ == '__main__':
                print('Сеанс номер {0} перенесен и помечен как выгруженный'.format(d[0]))
        else:
            if __name__ == '__main__':
                print('Места с таким id ({0}) в базе мест не существует'.format(d[5]))



if __name__ == '__main__':
    print(' -------- Отрабатываем фильмы --------------- ')
    print(' ------ Проверяем сеансы ------- ')
    check_db_seans()
    print(' ------ Корректируем по базе "верно-неверно" ------- ')
    correct_db_seans(correct_from_wrongright_db=True)
    print(' ------ Проставляем id сеансам ------- ')
    seans_name_to_event_id()
    print(' ------ Переносим спарсенные сеансы в основную базу ------- ')
    kino_seans_to_real_db()

    print('-------- Отрабатываем все остальные события --------------- ')
    print(' --------- Переносим спарсенные мероприятия в основную базу ----------- ')
    pars_event_to_db()
    print(' --------- Проставляем id сеансам ----------- ')
    event_set_event_id()
    print(' --------- Переносим спарсенные сеансы в основную базу ----------- ')
    event_seans_to_real_db()