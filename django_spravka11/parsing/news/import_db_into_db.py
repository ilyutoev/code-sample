import pymysql
import json
from datetime import datetime, timedelta
import os

print('\n-- Импорт базы данных из временной в постоянную -  ' + str(datetime.now()))

db = pymysql.connect(host="localhost", user="spravuser", passwd="12spr23FFd33", db="spravka11", charset="utf8")
cursor = db.cursor()

dalshe = True

while dalshe:
    #считываем из базы строки не загруженные ранее, отсортированные по дате по 100 штук
    posts = []
    sql = """SELECT id, title, content, date_pub, category_id, teaser, photo FROM pars_news where `import` = 0 ORDER BY date_pub LIMIT 100"""
    cursor.execute(sql)
    data = cursor.fetchall()
    if data:
        for dat in data:
            posts.append({'id':dat[0]})
            anons = dat[5]
            if len(anons) > 250:
                anons = anons[:anons.find('.')]
            sql2 = """INSERT INTO news_news (title, announcement, text, pub_date, category_id, photo) VALUES ('{title}', '{announcement}', '{text}', '{pub_date}', {category_id}, '{photo}')""".format(title=dat[1], announcement=anons, text=dat[2], pub_date=dat[3], category_id=dat[4], photo=dat[6])
            cursor.execute(sql2)
            db.commit()
        
        #отмечаем, что строки выгружены в файл
        for i in posts:
            sql3 = """UPDATE pars_news SET import = 1 WHERE id = {id}""".format(id=i['id'])
            cursor.execute(sql3)
            db.commit()

        print('Новости в базу данных сайта загужены, выгруженные новости отмечены.')

    else:
        dalshe = False

deldate = datetime.now() - timedelta(days=60)

sql = """DELETE FROM pars_news WHERE date_pub <= '{0}'""".format(deldate)
cursor.execute(sql)
db.commit()

db.close()