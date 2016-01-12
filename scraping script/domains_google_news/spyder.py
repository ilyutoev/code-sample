import logging
from grab.spider import Spider, Task
from grab import Grab
import re
import pymysql
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, create_engine, Date
from sqlalchemy.orm import sessionmaker
import random
import json
import threading
from datetime import datetime
from tools import send_domain_from_mail

LOCK = threading.RLock()

engine = create_engine("mysql+pymysql://root:@localhost/domains?charset=utf8", encoding='utf8', echo=False)

Base = declarative_base()
class Domains(Base):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True)
    domain = Column(String(255), unique=True)
    indexed = Column(Integer)
    date = Column(Date)

    def __repr__(self):
        return "<Domains(id='%s', domain='%s')>" % (self.id, self.domain)

Base.metadata.create_all(engine) 
Session = sessionmaker(bind=engine)

counter = 1

def step_parsing(num):
    global counter
    global LOCK

    check1 = True
    while check1:
        try:
            #path for proxy file
            proxfile = open('/home/domains/proxy.txt', 'r')
            proxline = random.choice([line for line in proxfile])[:-1]
            proxfile.close()
            #print(num, 'Ставим прокси', proxline)

            g = Grab()
            g.setup(proxy=proxline, timeout=5, connect_timeout=5)
            g.go('https://www.google.com/uds/GnewsSearch?callback=google.search.NewsSearch.RawCompletion&rsz=small&hl=ru&gss=.com&q=site%3Aobama&context=0&key=notsupplied&v=1.0')
            check = True
        except:
            #print('   Connection error')
            check = False

        if check:

            LOCK.acquire()
            session = Session()
            domains = session.query(Domains.id, Domains.domain).filter(Domains.indexed==None)[num*100:(num+1)*100-1]
            session.close()
            LOCK.release()

            if domains:
                for domain in domains:
        
                    try:
                        res = g.go('https://www.google.com/uds/GnewsSearch?callback=google.search.NewsSearch.RawCompletion&rsz=small&hl=ru&gss=.com&q=site%3A{0}&context=0&key=notsupplied&v=1.0'.format(domain.domain))
                        #print(counter, num, 'Go to domain', domain.domain)
                        counter += 1
                    except:
                        #print('   Connection error')
                        break

                    content = str(res.body)

                    if '"results":[]' in content:
                        dom = session.query(Domains).filter(Domains.id==domain.id).first()
                        dom.indexed = 0
                        session.add(dom)
                        session.commit()
                        session.close()
                        #print('   domain', domain.domain, 'not indexed', num,)

                    elif 'HTTP ERROR: 400' in content:
                        pass

                    elif content.count(domain.domain) >= 2:
                        if 'DomainMarket.com' in content:
                            dom = session.query(Domains).filter(Domains.id==domain.id).first()
                            dom.indexed = 0
                            session.add(dom)
                            session.commit()
                            session.close()
                            #print('   domain', domain.domain, 'not indexed', num,)
                        else:     
                            dom = session.query(Domains).filter(Domains.id==domain.id).first()
                            dom.indexed = 1
                            session.add(dom)
                            session.commit()
                            session.close()

                            LOCK.acquire()
                            fwrite = open('/home/domains/log/' + datetime.today().strftime('%Y%m%d') + '.txt', 'a')
                            fwrite.write('Domain ' + str(domain.domain) + ' indexed by G.News' + '\n')
                            fwrite.write('\n' + str(res.body) + '\n')
                            fwrite.close()
                            
                            send_domain_from_mail()
                            LOCK.release()

                            #print('   domain', domain.domain, 'indexed by G.News', num,)
                            #print('\n' ,str(res.body), '\n')
                    
                    elif content.count(domain.domain) == 1:
                        dom = session.query(Domains).filter(Domains.id==domain.id).first()
                        dom.indexed = 0
                        session.add(dom)
                        session.commit()
                        session.close()
                        #print('   domain', domain.domain, 'wtf', num,)

                    else:
                        #print('!!!  Something wrong', num,)
                        #print(str(res.body))
                        session.close()
                        break

            else:
                #print(num, '!! All domains checked')
                check1 = False


for x in range(15):
    threading.Thread(target=step_parsing, name="t" + str(x), args=[x]).start()
