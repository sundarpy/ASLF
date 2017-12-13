import sys, os, csv, re, json
import feedparser
import requests
import time
import schedule
from elasticsearch import Elasticsearch
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# #=====================================#
project_dir = "/home/sundar/Desktop/ASLF/feed"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'feed.settings'

import django
django.setup()
from appes.models import Myfeed
#====================================#
def My_Feed(file_obj):
    reader = csv.reader(file_obj, delimiter=',')
    i = 0
    count = 0
    extr_link = [] 
    fil_links = []
    ori_list = []   
    for line in reader:
        for each in line:
            if 'https' in each:
                extr_link.append(each)
            for data in extr_link: #Remove Duplicates from source.
                new_feed = data
                if new_feed not in fil_links:
                    fil_links.append(data)
                    origin = fil_links
                else:
                    pass
    for each in fil_links:
        d = feedparser.parse(each)
        nls_feed = []
        for item in d['items']:
            try:
                if 'link' in item:
                    ls_feed =  item['link']
                else:
                    ls_feed = None
                if 'title' in  item:
                    ts_feed =  item['title']
                else:
                    ts_feed = None
                if 'category' in item:
                    c_feed = item['category']
                else:
                    c_feed = 'others'
                if 'id' in  item:
                    id_feed =  item['id']
                else:
                    id_feed = None
                if 'updated' in item:
                    updates =  item['updated']
                else:
                    updates = None
                if 'published' in item:
                    p_feed =  item['published']
                else:
                    p_feed = None
                if 'description' in item:
                    des_feed =  item['description'] 
                    remo_uf = des_feed.decode('utf-8', 'ignore')
                    deatil = remo_uf
                else:
                    deatil = None
                #======================#
                myfeed = Myfeed.objects.create()
                myfeed.category = c_feed
                myfeed.main_link = each
                myfeed.description = deatil
                myfeed.title = ts_feed
                myfeed.sub_link = ls_feed
                myfeed.updated = updates
                myfeed.tag_id = id_feed
                myfeed.published = p_feed
                myfeed.save()
                i += 1
                
                #======================#
            except KeyError:
                pass
    return fil_links
def refeed():
    with open('/home/aptus/rssfeeds/ASLF/feed/import.csv', 'a+') as f_obj:
        My_Feed(f_obj)

# def duplicate():
#     refeed()
#     if fil_links not in refeed:
#         print('data is not there!')

if __name__ == "__main__":
    refeed()
    schedule.every(30).minutes.do(refeed)

    # while 1:
    #     schedule.run_pending()
    #     time.sleep(1)

#==============================Updated.6.2.apts#
