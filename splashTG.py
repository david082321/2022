# -*- coding: utf-8 -*-
import requests
import json
import os
import time
import math
import urllib
import datetime

f = open('splashTG_report.txt','w')
f.write("123")
f.close()

def timestamp_datetime(value):
    format = '%Y-%m-%d'
    value = time.localtime(value).replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    dt = time.strftime(format, value)
    return dt
def timestamp_datetimeHM(value):
    format = '%Y-%m-%d %H:%M'
    value = time.localtime(value).replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    dt = time.strftime(format, value)
    return dt
def timestamp_datetimeHMS(value):
    format = '%Y-%m-%d_%H-%M-%S'
    value = time.localtime(value).replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    dt = time.strftime(format, value)
    return dt

def LoadJsonOnly():
    birth = str(datetime.datetime.now(tz=timezone(timedelta(hours=8))).strftime('%m%d')) #"0101"
    url = "http://app.bilibili.com/x/v2/splash/list?appkey=1d8b6e7d45233436&build=996000200&mobi_app=android&width=1080&height=1920&birth=" + str(birth)
    r = requests.get(url)
    if (r.status_code!=200):
        print(r.status_code)
        time.sleep(10)
    datajson = r.json()['data']['list']
    url2 = "https://app.bilibili.com/x/v2/splash/list?appkey=1d8b6e7d45233436&build=996000200&mobi_app=ipad&platform=ios&width=0&height=0&birth=" + str(birth)
    r2 = requests.get(url2)
    jscontent2 = r2.content.decode("utf-8")
    datajson2 = json.loads(str(jscontent2))['data']['list']
    max2 = len(datajson2)
    for item in datajson:
        iid = item['id']
        thumb = item['thumb']
        begin_time = timestamp_datetime(int(item['begin_time'])+28800)
        end_time = timestamp_datetime(int(item['end_time'])+28800)
        if (begin_time==end_time):
            my_time=str(begin_time)
        else:
            begin_time = timestamp_datetimeHM(int(item['begin_time'])+28800)
            end_time = timestamp_datetimeHM(int(item['end_time'])+28800)
            my_time=str(begin_time)+' 至 '+str(end_time)
        uri = item['uri']
        uri_title = item['uri_title']
        try:
            video_url = item['video_url']
            if video_url is None:
                hasvideo = 0
            else:
                hasvideo = 1
        except KeyError:
            hasvideo = 0
        
        thumb2 = ""
        for i2 in range(0,max2):
            iid2 = datajson2[i2]['id']
            if iid == iid2:
                thumb2 = datajson2[i2]['thumb']

        show_title = ""
        show_title2 = ""
        show_thumb = ""
        show_thumb2 = ""
        show_video = ""
        show_video2 = ""
        if (str(uri_title) != ""):
            show_title = '\r\n标语：'+str(uri_title)
            show_title2 = '%0d%0a'+urllib.parse.quote('标语：'+str(uri_title))
        if (hasvideo == 1):
            show_video = '\r\n视频：'+str(video_url)
            show_video2 = '%0d%0a'+urllib.parse.quote('视频：'+str(video_url))
        else:
            if (thumb2 == ""):
                show_thumb = '\r\n图片：'+str(thumb)
                show_thumb2 = '%0d%0a'+urllib.parse.quote('图片：'+str(thumb))
            else:
                show_thumb = '\r\n大图：'+str(thumb2)+'\r\n小图：'+str(thumb)
                show_thumb2 = '%0d%0a'+urllib.parse.quote('大图：'+str(thumb2))+'%0d%0a'+urllib.parse.quote('小图：'+str(thumb))

        writetext = 'ID：'+str(iid)+'\r\n日期：'+str(my_time)+show_title+show_thumb+'\r\n入口：'+str(uri)+show_video
        writetext2 = urllib.parse.quote('ID：'+str(iid))+'%0d%0a'+urllib.parse.quote('日期：'+str(my_time))+show_title2+show_thumb2+'%0d%0a'+urllib.parse.quote('入口：'+str(uri))+show_video2

        writejson = 'id/send/'+str(iid)+'.txt'
        if os.path.isfile(writejson):
            if ( str(open(writejson,'r').read()) !=str(writetext).replace('\r', '') ):
                writeAndsend=1
                print("E")
                #print(open(writejson,'r').read())
                #print(str(writetext))
            else:
                writeAndsend=0
        else:
            writeAndsend=1
        
        if (writeAndsend==1):
            if (open('splashTG_report.txt','r').read()=="123"):
                f = open('splashTG_report.txt','w')
                f.write("")
                f.close()
            f = open('splashTG_report.txt','a')
            f.write(writetext+'\r\n\r\n')
            f.close()
            print("writeAndsend")
            try:
                f = open(writejson,'w')
                f.write(writetext)
                f.close()
            except ValueError:
                print("error")
                pass
            bottoken = os.environ["token"]
            url = 'https://api.telegram.org/bot'+bottoken+'/sendMessage?chat_id=-1001213651238&text='+urllib.parse.quote(writetext)
            r = requests.get(url)
            
            if (hasvideo == 0):
                docu = thumb
            else:
                docu = video_url
            url2 = 'https://api.telegram.org/bot'+bottoken+'/sendDocument?chat_id=-1001213651238&document='+urllib.parse.quote(docu)
            r2 = requests.get(url2)
    time.sleep(1)

LoadJsonOnly()
print('Finish')
