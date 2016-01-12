from grab.spider import Spider, Task
from grab import Grab, error
import time
import os
import csv
import pymysql

from tools import add_file_to_db

g = Grab()
#g.setup(proxy='192.168.1.1:3128', timeout=120)
g.setup(timeout=360)

files_path = os.getcwd() + '/files/namejet/'


#www.namejet.com
#0 step - unarhive files
print(' - Deleted all files in folder')
file_list = os.listdir(files_path)

for domain_file in file_list:
    os.remove(files_path + domain_file)
    print('   file deleted')

# 1 step - download files
print('Open www.namejet.com')
g.go('http://www.namejet.com/Pages/Downloads.aspx')
value_viewstate = g.doc.select('//input[@id="__VIEWSTATE"]').attr('value')
value_eventvalidation = g.doc.select('//input[@id="__EVENTVALIDATION"]').attr('value')

#Get id for download domains fo delete
domain_delete_id_list = g.doc.select('//div[@class="sCol sCol5"]//li[contains(@id,"Delete")]/a')

'''
domains_id_list = [
    'ctl00$ContentPlaceHolder1$hlPreReleaseAll'
    ]

for domain_delete_id in domain_delete_id_list:
    domains_id_list.append(domain_delete_id.attr('href').replace("javascript:__doPostBack('", "").replace("','')", ""))

print(' - Start download files')

print(domains_id_list)
for domain_id in domains_id_list:
    resp = g.go('http://www.namejet.com/Pages/Downloads.aspx', post={
            '__EVENTTARGET': domain_id,
            '__EVENTARGUMENT': '',
            '__VIEWSTATE' : value_viewstate,
            '__EVENTVALIDATION': value_eventvalidation,
            'ctl00$TextBoxSearch': 'Search Domains',
            'ctl00$HiddenFieldFristNav': ''})

    filename = g.response.headers['Content-Disposition'].split('=')[1]
    g.response.save(files_path + filename)
    print('   File downloaded', filename)
    print('   Sleep 20 sec.')
    time.sleep(20)
'''

link_to_site = 'http://www.namejet.com'

domains_files_list = [
    '/download/PreRelease.txt'
    ]

for domain_delete_id in domain_delete_id_list:
    domains_files_list.append(domain_delete_id.attr('href').replace("javascript:__doPostBack('", "").replace("','')", ""))

for domain in domains_files_list:
    g.go(link_to_site + domain)

    print(link_to_site + domain)

    g.response.save(files_path + domain.split('/')[-1])
    print('   File downloaded', domain)
    print('   Sleep 20 sec.')
    time.sleep(20)

#error.GrabTimeoutError - сделать try и посылать опять на закачку - 5 итераций


# 2 step - fixing PreRelease.txt file
print(' - Fixing PreRelease.txt file')
prerelease_path = files_path + 'PreRelease.txt'

if os.path.exists(prerelease_path):
    f = open(files_path + 'PreRelease2.txt', 'w')
    with open(prerelease_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            f.write(row[0] + '\r\n')
    f.close()
    os.remove(prerelease_path)
    print('   PreRelease.txt file fixed and deleted')
else:
    print('   PreRelease.txt file does not exist')


# 3 step - add domains to mysql
print(' - Import csv files to db')
file_list = os.listdir(files_path)

for domain_file in file_list:
    add_file_to_db(files_path + domain_file)
    


