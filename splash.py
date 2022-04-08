# -*- coding: utf-8 -*-
import requests
import random
import json
import os
import time
import math
import urllib
import datetime
import ssl
err = 0
path = 'splash'
if not os.path.isdir(path):
    os.mkdir(path)
path = 'splash2'
if not os.path.isdir(path):
    os.mkdir(path)
def timestamp_folder(value):
    format = '%Y-%m'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt
def timestamp_datetime(value):
    format = '%Y-%m-%d'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt
def timestamp_datetimeHMS(value):
    format = '%Y-%m-%d_%H-%M-%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

def LoadJsonOnly(raltion,mobi_app,width,height,listName,listName2):
    fileName = raltion
    if mobi_app=="android":
        platform = "android"
    else:
        platform = "ios"
    birth = str(datetime.datetime.now().strftime('%m%d')) #"0101"
    url = 'http://app.bilibili.com/x/v2/splash/list?appkey=1d8b6e7d45233436&build=999999999&mobi_app=' + str(mobi_app) + '&platform='+str(platform) + '&width='+str(width)+'&height='+str(height) + "&birth=" + str(birth)
    print(str(fileName))
    r = requests.get(url)
    if (r.status_code!=200):
        print(r.status_code)
        time.sleep(60)
    datajson = r.json()['data']['list']
    max = len(datajson)
    for i in range(0,max):
        iid = datajson[i]['id']
        thumb = datajson[i]['thumb']
        begin_time = timestamp_datetime(datajson[i]['begin_time'])
        end_time = timestamp_datetime(datajson[i]['end_time'])
        uri = datajson[i]['uri']
        img_format = thumb.split('.')[-1]
        try:
            f = open(listName,'a')
            f.write('"'+str(fileName)+'","'+str(thumb)+'","'+str(uri)+'","'+str(begin_time)+'","'+str(end_time)+'","'+str(iid)+'"\n')
            f.close()
        except ValueError:
            err = err + 1
            print("Error. Wait 60 seconds.\t" + str(err))
            time.sleep(60)
            pass
        writejson = listName2+'/'+str(begin_time)+'_'+str(iid)+'.json'
        try:
            f = open(writejson,'a+')
            f.write(str(fileName)+'　'+str(thumb)+'　'+str(uri)+'\n')
            f.close()
        except ValueError:
            pass
    time.sleep(1)

def LoadImg(raltion,mobi_app,width,height,listName,listName2):
    path = 'splash/'+str(raltion)
    if not os.path.isdir(path):
        os.mkdir(path)
    birth = str(datetime.datetime.now().strftime('%m%d')) #"0101"
    #url = 'http://app.bilibili.com/x/v2/splash/list?build='+ str(LoadVer()) +'&mobi_app=' + str(mobi_app) + '&width='+str(width)+'&height='+str(height)
    url = 'http://app.bilibili.com/x/v2/splash/list?appkey=1d8b6e7d45233436&build=999999999&mobi_app=' + str(mobi_app) + '&width='+str(width)+'&height='+str(height) + "&birth=" + str(birth)
    print(str(raltion))
    r = requests.get(url)
    if (r.status_code!=200):
        print(r.status_code)
        time.sleep(10)
    datajson = r.json()['data']['list']
    for item in datajson:
        iid = item['id']
        thumb = item['thumb']
        begin_time = timestamp_datetime(item['begin_time'])
        end_time = timestamp_datetime(item['end_time'])        
        uri = item['uri']
        
        folder = timestamp_folder(item['begin_time'])
        pathWithMonth = path + '/' + folder
        if not os.path.isdir(pathWithMonth):
            os.mkdir(pathWithMonth)
        try:
            video_url = item['video_url']
            filename = pathWithMonth + '/' + str(begin_time)+'_'+str(iid) + '.mp4'
            downloadthumb = video_url
        except KeyError:
            img_format = thumb.split('.')[-1]
            filename = pathWithMonth+ '/' + str(begin_time)+'_'+str(iid) + '.' + img_format
            downloadthumb = thumb
        if os.path.exists(filename):
            time.sleep(0.5)
        else:
            print('write: '+str(iid))
            ssl._create_default_https_context = ssl._create_unverified_context
            f = urllib.request.urlopen(downloadthumb)
            with open(filename, "wb") as fff:
                fff.write(f.read())
        try:
            f = open(listName,'a')
            f.write('"'+str(raltion)+'","'+str(thumb)+'","'+str(uri)+'","'+str(begin_time)+'","'+str(end_time)+'","'+str(iid)+'"\n')
            f.close()
        except ValueError:
            err = err + 1
            print("Error. Wait 60 seconds.\t" + str(err))
            time.sleep(60)
            pass
        writejson = listName2+'/'+str(begin_time)+'_'+str(iid)+'.json'
        try:
            f = open(writejson,'a+')
            f.write(str(raltion)+'　'+str(thumb)+'　'+str(uri)+'\n')
            f.close()
        except ValueError:
            pass
    time.sleep(1)

def LoadImgbrand(raltion,listName3):
    path = 'splash3/'+str(raltion)
    if not os.path.isdir(path):
        os.mkdir(path)
    fileName = raltion
    if str(raltion) == "1080x1920":
    	url = 'https://app.bilibili.com/x/v2/splash/brand/list?access_key=&appkey=1d8b6e7d45233436&build=6110500&mobi_app=android&platform=android&screen_height=1920&screen_width=1080&ts=1600000000&sign=3f8d82831a799c14c29efcade745dea3'
    elif str(raltion) == "1600x2560":
    	url = 'https://app.bilibili.com/x/v2/splash/brand/list?actionKey=appkey&appkey=27eb53fc9058f8c3&build=10350&device=phone&mobi_app=iphone&network=wifi&platform=ios&s_locale=zh-Hant_TW&screen_height=1136&screen_width=640&sign=a7be98df5fad7d581aa0c2781b96fc24&statistics=%7B%22appId%22%3A1%2C%22version%22%3A%226.13.0%22%2C%22abtest%22%3A%22%22%2C%22platform%22%3A1%7D&ts=1609120708'
    else:
    	url = 'https://app.bilibili.com/x/v2/splash/brand/list?access_key=&appkey=1d8b6e7d45233436&build=6110500&mobi_app=ipad&platform=ipad&screen_height=1080&screen_width=1920&ts=1600000000&sign=5f2aa184e0c0b7aa8e8034b392b4e32b'
    print(str(fileName))
    r = requests.get(url)
    if (r.status_code!=200):
        print(r.status_code)
        time.sleep(60)
    datajson = r.json()['data']['list']
    max = len(datajson)
    for i in range(0,max):
        iid = datajson[i]['id']
        thumb = datajson[i]['thumb']
        logo_url = datajson[i]['logo_url']
        mode = datajson[i]['mode']
        #thumb
        img_format = thumb.split('.')[-1]
        filename = 'splash3/' + fileName + '/' + str(iid) + '.' + img_format
        downloadthumb = thumb
        print(filename)
        if os.path.exists(filename):
            time.sleep(0.5)
        else:
            print('write: '+str(iid))
            ssl._create_default_https_context = ssl._create_unverified_context
            f = urllib.request.urlopen(downloadthumb)
            with open(filename, "wb") as fff:
                fff.write(f.read())
            writetext = 'ID：'+str(iid)+'\r\n图片：'+str(thumb)
            bottoken = os.environ["token"]
            url = 'https://api.telegram.org/bot'+bottoken+'/sendMessage?chat_id=-1001213651238&text='+urllib.parse.quote(writetext)
            if str(raltion) != "1080x1920":
                r = requests.get(url)
        #logo
        img_format = logo_url.split('.')[-1]
        filename = 'splash3/' +fileName + '/' + str(iid) + '_logo.' + img_format
        if os.path.exists(filename):
            time.sleep(0.5)
        else:
            print('writeLOGO: '+str(iid))
            ssl._create_default_https_context = ssl._create_unverified_context
            f = urllib.request.urlopen(logo_url)
            with open(filename, "wb") as fff:
                fff.write(f.read())
        try:
            f = open(listName3,'a')
            f.write('"'+str(iid)+'","'+str(fileName)+'","'+str(thumb)+'","'+str(logo_url)+'","'+str(mode)+'"\n')
            f.close()
        except ValueError:
            err = err + 1
            print("Error. Wait 60 seconds.\t" + str(err))
            time.sleep(60)
            pass
    time.sleep(1)

def LoadJson(raltion,mobi_app,width,height,jsonName):
    birth = str(datetime.datetime.now().strftime('%m%d')) #"0101"
    url = 'http://app.bilibili.com/x/v2/splash/list?appkey=1d8b6e7d45233436&build=999999999&mobi_app=' + str(mobi_app) + '&width='+str(width)+'&height='+str(height) + "&birth=" + str(birth)
    r = requests.get(url)
    f = open(jsonName,'wt')
    f.write(r.content.decode("utf-8"))
    f.close()

def doSth():
    datenow = datetime.datetime.now()
    path = 'splash2/'+str(datenow.strftime("%Y-%m-%d"))
    jsonName = 'splash2/'+str(datenow.strftime("%Y-%m-%d"))+'/'+ str(datenow.strftime("%Y-%m-%d %H-%M"))+'.json'
    listName = 'splash2/'+str(datenow.strftime("%Y-%m-%d"))+'/'+ str(datenow.strftime("%Y-%m-%d %H-%M")) +'.csv'
    if not os.path.isdir(path):
        os.mkdir(path)
    listName2 = 'id/'+str(datenow.strftime("%Y-%m-%d %H-%M"))
    if not os.path.isdir(listName2):
        os.mkdir(listName2)
    path2 = 'splash4/'+str(datenow.strftime("%Y-%m-%d"))
    listName3 = 'splash4/'+str(datenow.strftime("%Y-%m-%d"))+'/'+ str(datenow.strftime("%Y-%m-%d %H-%M")) +'.csv'
    
    LoadJson('1080x1920','android','1080','1920',jsonName)
    LoadJsonOnly('320x480','android','200','300',listName,listName2)
    LoadJsonOnly('375x647','android','400','700',listName,listName2)
    LoadJsonOnly('480x640','android','300','400',listName,listName2)
    LoadJsonOnly('480x728','android','2900','4400',listName,listName2)
    LoadJsonOnly('480x800','android','300','500',listName,listName2)
    LoadJsonOnly('480x854','android','0','100',listName,listName2)
    LoadJsonOnly('600x976','android','800','1300',listName,listName2)
    LoadJsonOnly('640x960','android','600','900',listName,listName2)
    LoadJsonOnly('640x1136','android','1300','2300',listName,listName2)
    LoadJsonOnly('720x1184','android','1100','1800',listName,listName2)
    LoadJsonOnly('720x1208','android','1000','1700',listName,listName2)
    LoadJsonOnly('720x1280','android','900','1600',listName,listName2)
    LoadJsonOnly('750x1334','iphone','500','900',listName,listName2)
    LoadJsonOnly('768x976','android','0','0',listName,listName2)
    LoadJsonOnly('768x1024','android','900','1200',listName,listName2)
    LoadJsonOnly('768x1280','android','900','1500',listName,listName2)
    LoadJsonOnly('800x1216','android','1700','2600',listName,listName2)
    LoadJsonOnly('800x1232','android','900','1400',listName,listName2)
    LoadJsonOnly('800x1280','android','500','800',listName,listName2)
    LoadJsonOnly('1024x768','ipad','400','300',listName,listName2)
    LoadJsonOnly('1080x1776','android','1700','2800',listName,listName2)
    LoadImg('1080x1920','android','1080','1920',listName,listName2)
    LoadJsonOnly('1125x2436','iphone','0','100',listName,listName2)
    LoadJsonOnly('1152x1920','android','1200','2000',listName,listName2)
    LoadJsonOnly('1242x2208','iphone','900','1600',listName,listName2)
    LoadJsonOnly('1440x2560','android','1800','3200',listName,listName2)
    LoadJsonOnly('1536x2048','android','1500','2000',listName,listName2)
    LoadJsonOnly('1536x2560','android','1500','2500',listName,listName2)
    LoadJsonOnly('1600x2560','android','1500','2400',listName,listName2)
    LoadJsonOnly('2048x1536','ipad','0','100',listName,listName2)
    LoadImg('2048x2732','android','500','700',listName,listName2)
    LoadImg('2732x2048','ipad','0','0',listName,listName2)
    
    if not os.path.isdir(path2):
        os.mkdir(path2)
    LoadImgbrand('1080x1920',listName3)
    LoadImgbrand('1600x2560',listName3)
    LoadImgbrand('2732x2048',listName3)
    
    print('Finish')

r = requests.get(os.environ["biliapk"])
doSth()
