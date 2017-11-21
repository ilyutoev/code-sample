from purifier.purifier import HTMLPurifier
import os
import json
import pymysql
import string
from unidecode import unidecode
import re
import datetime
from PIL import Image

purif = HTMLPurifier()

#картинки в новостях дажнго
#картинки в тексте - /media/uploads/img_0009.jpg
#картинка для анонса - news/2015/03/22/1.jpg

'''
Установка:
pip install -e git+git://github.com/ilyutoev/python-html-purifier#egg=python-html-purifier

sudo apt-get install libcurl4-openssl-dev

sudo apt-get install libxml2-dev
sudo apt-get install libxslt1-dev 
pip install -U Grab

'''


#функция преобразования даты и времени, полученной при парсинге комиинформа в формат пригодный для записи в бд 2014-08-15 14:00:00
def data_change(inputstring, source):
    if source == 'komiinform':
        month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'
    }
        outputstring = inputstring.replace(",", "")
        outputstring = outputstring.replace("г.", "")
        outputstring = outputstring.replace("года ", "")
        array = outputstring.split(" ")
        if len(array[0]) == 1:
            array[0] = '0' + array[0]
        outputstring = array[2] + '-' + month[array[1]] + '-' + array[0] + ' ' + array[3]
        return outputstring

    if source == 'bnkomi':
        temp = inputstring.split(' ')
        temp2 = temp[0].split('.')
        return temp2[2] + '-' + temp2[1] + '-' + temp2[0] + ' ' + temp[1]

    if source == 'komiopera':
        month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'
    }
        array = inputstring.lower().split(" ")
        if len(array[0]) == 1:
            array[0] = '0' + array[0]
        inputstring = array[2] + '-' + month[array[1]] + '-' + array[0]
        return inputstring

#функция создания вложенных папок из даты вида 2014/08/11/. Принимает дату - возвращает путь к папке
def create_img_folder(date, type='news'):
    data_for_folder = date.split("-")
    if type == 'news':
        pathtoimgfolder = '/home/spravka/projects/spravka11/media/news/' + data_for_folder[0] + '/' + data_for_folder[1] + '/' + data_for_folder[2][:2]
    if type == 'event':
        pathtoimgfolder = '/home/spravka/projects/spravka11/media/events/' + data_for_folder[0] + '/' + data_for_folder[1] + '/' + data_for_folder[2][:2]
    try:
        os.makedirs(pathtoimgfolder)
    except OSError:
        pass
    return pathtoimgfolder

#функция чистит текст от юникодных спецсимволов и заменяет их на спецкоды html
def clean_text(text,type):
    htmlcodes = ['&Aacute;', '&aacute;', '&Agrave;', '&Acirc;', '&agrave;', '&Acirc;', '&acirc;', '&Auml;', '&auml;', '&Atilde;', '&atilde;', '&Aring;', '&aring;', '&Aelig;', '&aelig;', '&Ccedil;', '&ccedil;', '&Eth;', '&eth;', '&Eacute;', '&eacute;', '&Egrave;', '&egrave;', '&Ecirc;', '&ecirc;', '&Euml;', '&euml;', '&Iacute;', '&iacute;', '&Igrave;', '&igrave;', '&Icirc;', '&icirc;', '&Iuml;', '&iuml;', '&Ntilde;', '&ntilde;', '&Oacute;', '&oacute;', '&Ograve;', '&ograve;', '&Ocirc;', '&ocirc;', '&Ouml;', '&ouml;', '&Otilde;', '&otilde;', '&Oslash;', '&oslash;', '&szlig;', '&Thorn;', '&thorn;', '&Uacute;', '&uacute;', '&Ugrave;', '&ugrave;', '&Ucirc;', '&ucirc;', '&Uuml;', '&uuml;', '&Yacute;', '&yacute;', '&yuml;', '&copy;', '&reg;', '&trade;', '&euro;', '&cent;', '&pound;', '&lsquo;', "", '&ldquo;', '&rdquo;', '"', '"', '&mdash;', '-', '&deg;', '&plusmn;', '&frac14;', '&frac12;', '&frac34;', '&times;', '&divide;', '&alpha;', '&beta;', '&infin','']
    htmlcodes2 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '"', '"', '', '', '', '', '', '', '', '', '', '', '', '','']
    funnychars = ['\xc1','\xe1','\xc0','\xc2','\xe0','\xc2','\xe2','\xc4','\xe4','\xc3','\xe3','\xc5','\xe5','\xc6','\xe6','\xc7','\xe7','\xd0','\xf0','\xc9','\xe9','\xc8','\xe8','\xca','\xea','\xcb','\xeb','\xcd','\xed','\xcc','\xec','\xce','\xee','\xcf','\xef','\xd1','\xf1','\xd3','\xf3','\xd2','\xf2','\xd4','\xf4','\xd6','\xf6','\xd5','\xf5','\xd8','\xf8','\xdf','\xde','\xfe','\xda','\xfa','\xd9','\xf9','\xdb','\xfb','\xdc','\xfc','\xdd','\xfd','\xff','\xa9','\xae','\u2122','\u20ac','\xa2','\xa3','\u2018','\u2019','\u201c','\u201d','\xab','\xbb','\u2014','\u2013','\xb0','\xb1','\xbc','\xbd','\xbe','\xd7','\xf7','\u03b1','\u03b2','\u221e', '\u20cf']
    newtext = ''
    if type == 'shingle':
        for char in text:
            if char not in funnychars:
                newtext = newtext + str(char)
            else:
                newtext  = newtext + htmlcodes2[funnychars.index(char)]
    if type == 'normal':
        for char in text:
            if char not in funnychars:
                newtext = newtext + str(char)
            else:
                newtext  = newtext + htmlcodes[funnychars.index(char)]

    newtext = newtext.replace('<p></p>','') #убираем пустые абзацы
    return newtext

#добавляем копирайт внизу текста в соответствии с сайтом, с которого взята информация
def copyright(text, source):
    if source == 'komiinform':
        return text + '<p style="text-align:right;">По материалам ИА "Комиинформ"</p>'
    if source == 'bnkomi':
        return text + '<p style="text-align:right;">По материалам ИА "Север-Медиа"</p>'
    if source == 'komionline':
        return text + '<p style="text-align:right;">По материалам ИА "КомиОнлайн"</p>'
    if source == 'komikz':
        return text + '<p style="text-align:right;">По материалам ЗАО "Газета "Красное знамя"</p>'

#функция возвращает id по полученой рубрике для записи в бд
def rubrics_id(rubrica, source):
    '''
    Общество 3
    Экономика 1 
    Политика 2
    Происшествия 4
    Право 5
    Спорт 6
    Культура 7
    Окружающая среда 9
    Образование 8
    '''

    komiinform_rubrics = {
        'Общество': 3,
        'Экономика': 1,
        'Политика': 2,
        'Происшествия': 4,
        'Право': 5,
        'Спорт': 6,
        'Экология': 9,
        'Культура': 7,
        'Соседи': 3,
        'Погода': 9
    }
    if source == 'komiinform':
        try:
            return komiinform_rubrics[rubrica]
        except KeyError:
            return 2

    bnkomi_rubrics = {
        'ПОЛИТИКА': 2,
        'ЭКОНОМИКА': 1,
        'ОБЩЕСТВО': 3,
        'ЭКОЛОГИЯ': 9,
        'ПРАВО': 5,
        'СПОРТ': 6,
        'КУЛЬТУРА': 7,
        'ПРОИСШЕСТВИЯ': 4,
        'РЕПОРТАЖ': 3
    }
    if source == 'bnkomi':
        try:
            return bnkomi_rubrics[rubrica]
        except KeyError:
            return 2
    
    komionline_rubrics = {
        'Факты': 3, #Art и 
        'Коми': 3, #Жизнь в 
        'жизни': 3, #Образ жизни
        'Отморошки': 3,
        'Пресс-релизы': 3,
        'Социум': 3
    }
    if source == 'komionline':
        try:
            return komionline_rubrics[rubrica]
        except KeyError:
            return 2

    komikz_rubrics = {
        'Политика': 2, 
        'Экономика': 1, 
        'Общество': 3,
        'Происшествия и криминал': 4,
        'Актуально': 3,
        'Культура': 7,
        'Спорт': 6,
        'Окружающая среда': 9,
        'Наука и образование': 8,
        'ЖКХ': 3
    }
    if source == 'komikz':
        try:
            return komikz_rubrics[rubrica]
        except KeyError:
            return 2


#функция делает список шинглов из текста и сериализует его в json
def genshingle(source, leng):
    import binascii
    source = purif.feed(source) #вычищаем все html теги
    source = clean_text(source,'shingle')
   
    shingleLen = leng #длина шингла
    out = [] 

    def canonize(source): #функция канонизации текста
        stop_symbols = '"’.,!?:;-\n\r()'
        stop_words = ('это', 'как', 'так',
        'и', 'в', 'над',
        'к', 'до', 'не',
        'на', 'но', 'за',
        'то', 'с', 'ли',
        'а', 'во', 'от',
        'со', 'для', 'о',
        'же', 'ну', 'вы',
        'бы', 'что', 'кто',
        'он', 'она')

        return ( [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)] )

    source = canonize(source)

    for i in range(len(source)-(shingleLen-1)):
        out.append (binascii.crc32(' '.join( [x for x in source[i:i+shingleLen]] ).encode('utf-8')))

    return json.dumps(out)  #c = json.loads(data[0][0]) - десереализация

def load_db_shingle(startdata, source):
    source_id = {
        'bnkomi': 2,
        'komionline':3,
        'komikz': 4
    }
    temp_date = startdata
    temp_date = temp_date.split(' ')
    start_date = temp_date[0] + ' 23:59:59'
    temp_date = temp_date[0].split('-')
    d = datetime.date(int(temp_date[0]),int(temp_date[1]),int(temp_date[2]))
    delta = datetime.timedelta(-7)
    finish_date = str(d + delta) + ' 00:00:00'

    db = pymysql.connect(host="localhost", user="user", passwd="password", db="dbname", charset="utf8")
    cursor = db.cursor()

    sql = """SELECT url, shingle_title, shingle_text FROM pars_news where `date_pub`>='{finish_date}' AND `date_pub`<='{start_date}' AND `id_source` != {source_id} ORDER BY date_pub""".format(start_date=start_date, finish_date=finish_date, source_id=source_id[source])
    cursor.execute(sql)
    data = cursor.fetchall()

    links = []
    shingle_title = []
    shingle_text = []
    for dat in data:
        links.append(dat[0])
        shingle_title.append(json.loads(dat[1]))
        shingle_text.append(json.loads(dat[2]))
    
    return links, shingle_title, shingle_text


def compaire(source1,source2):
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1

    return same*2/float(len(source1) + len(source2))*100

def write_news_to_db(dict_news):

    #настройки подключения к базе
    db = pymysql.connect(host="localhost", user="user", passwd="password", db="dbname", charset="utf8")

    #подготовка поля slug для базы - берем последний id из базы + url_translit
    cursor = db.cursor()

    #title, content, slug, seo_keys, seo_desc, date_pub, date_last_modified, user_idб category_id, teaser, photo - дальше мои поля: url, shingle_text, shingle_title,id_source
    sql = """INSERT INTO pars_news (title, content, date_pub, category_id, teaser, photo, url, shingle_text, shingle_title, id_source) VALUES ('{title}', '{content}', '{date_pub}', {category_id}, '{teaser}', '{photo}', '{url}', '{shingle_text}', '{shingle_title}', {id_source})""".format(title=dict_news['title'], content=dict_news['text'], date_pub=dict_news['date'], category_id=dict_news['rubr'], teaser=dict_news['anons'], photo=dict_news['img_anons'], url=dict_news['url'], shingle_text=dict_news['shingle_text'], shingle_title=dict_news['shingle_title'], id_source=dict_news['id_source'])
    #в запросе строки в кавычках числа без  - {}, '{}'

    # исполняем SQL-запрос
    cursor.execute(sql)
    # применяем изменения к базе данных
    db.commit()
    if __name__ == '__main__':
        return print('Запись в бд внесена - ' + dict_news['date'] + ' - ' + dict_news['url'])

#функция выборки последних 100 ссылок на спарсенные статьи для останова парсинга. возвращает писок ссылок
def last_ten_news_links(source):
    source_id = {
        'komiinform':1,
        'bnkomi': 2,
        'komionline': 3,
        'komikz': 4
    }
    db = pymysql.connect(host="localhost", user="user", passwd="password", db="dbname", charset="utf8")
    cursor = db.cursor()
    sql = """SELECT url FROM pars_news WHERE id_source={0} ORDER BY date_pub DESC LIMIT 100;""".format(source_id[source])
    cursor.execute(sql)
    data = cursor.fetchall()
    links = []
    for link in data:
        links.append(link[0])
    return links


def resize(filename, size, out, crop=False):
    im = Image.open(filename)
    if crop:
        width = im.size[0]
        height = im.size[1]
        if width > height:
            x = (width - height)//2
            y = height
            box = (x, 0, y+x, y)
        else:            
            x = (height - width)//2
            y = width
            box = (0, x, y, y + x)
        im = im.crop(box)
        im.thumbnail(size)
    else:
        im.thumbnail(size)
    im.save(out)

#функция записи события
def write_event_to_db(dict_news):
    #настройки подключения к базе
    db = pymysql.connect(host="localhost", user="user", passwd="password", db="dbname", charset="utf8")

    #подготовка поля slug для базы - берем последний id из базы + url_translit
    cursor = db.cursor()
    
    #name, date, time, type_event, type_film, price, place - source_id
    sql = """INSERT INTO pars_afisha (name, date, time, type_event, type_film, price, place, description, poster) VALUES ('{name}', '{date}', '{time}', '{type_event}', '{type_film}', {price}, {place}, '{description}', '{poster}' )""".format(name=dict_news['name'], date=dict_news['date'], time=dict_news['time'], type_event=dict_news['type_event'], type_film=dict_news['type_film'], price=dict_news['price'], place=dict_news['source_id'], description=dict_news['description'], poster=dict_news['poster'])
    #в запросе строки в кавычках числа без  - {}, '{}'

    # исполняем SQL-запрос
    cursor.execute(sql)
    # применяем изменения к базе данных
    db.commit()
    if __name__ == '__main__':
        return print('Запись в базу внесена')

#функция даты последних записанных в базу событий
def last_date_event(source, date):
    place = {
        'rublic':1,
        'maxi': 2,
        'mori': 3,
        'raduga': 4,
        'dramakomi': 5,
        'komiopera': 6,
        'filarmonia': 7,
        'autofilm': 8,
        'illuzion': 9,
        'renova':10,
        'sportrk': 11
    }
    db = pymysql.connect(host="localhost", user="user", passwd="password", db="dbname", charset="utf8")
    cursor = db.cursor()
    sql = """SELECT date FROM pars_afisha WHERE date >= '{0}' AND place={1};""".format(date, place[source])
    cursor.execute(sql)
    db_output = cursor.fetchall()
    dates = []
    for string in db_output:
        dates.append(str(string[0]))
    return dates

#запись в базу корневых событий
def write_core_event_to_db(dict_news):
    #настройки подключения к базе
    db = pymysql.connect(host="localhost", user="user", passwd="password", db="dbname", charset="utf8")

    #подготовка поля slug для базы - берем последний id из базы + url_translit
    cursor = db.cursor()
    
    '''
    Именованные параметры можно, также, развернуть из словаря, используя оператор **:

    >>> person = {'first':'Reuven', 'last':'Lerner'}
    >>> "Good morning, {first} {last}".format(**person)

    'Good morning, Reuven Lerner'
    '''

    sql = """INSERT INTO events_events (title, ganre, limit_year, poster, description, url, event_type_id) VALUES ("{title}", '{ganre}', '{limit_year}', '{poster}', '{description}', '{url}', {event_type})""".format(title=dict_news['title'], ganre=dict_news['ganre'], limit_year=dict_news['limit_year'], poster=dict_news['poster'], description=dict_news['description'], url=dict_news['url'], event_type=dict_news['event_type'])
    #в запросе строки в кавычках числа без  - {}, '{}'
            
    # исполняем SQL-запрос
    cursor.execute(sql)
    # применяем изменения к базе данных
    db.commit()
    if __name__ == '__main__':
        return print('Запись в базу внесена - ', dict_news['title'])

def last_core_event_links():
    db = pymysql.connect(host="localhost", user="user", passwd="password", db="dbname", charset="utf8")
    cursor = db.cursor()
    sql = """SELECT url FROM events_events;"""
    cursor.execute(sql)
    db_output = cursor.fetchall()
    dates = []
    for string in db_output:
        dates.append(str(string[0]))
    return dates