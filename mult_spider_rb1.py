#!usr/bin/python#coding=utf-8
import threading
import urllib
import sys
from bs4 import BeautifulSoup
import thread
import re
import Queue
import math

mutex = threading.Lock()

def getHtml(url):
    #print "主页为:"+url
    page = urllib.urlopen(url)
    html = page.read()
    return html.decode('gbk').encode("utf-8")

def getHtml2(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html  

def getPeoples(url):
    """
    获取所有的关注者的url
    """
    mainPage = getHtml(url)
    scdPageUrl = re.findall(r"关注的人.*?a href=\".*?\"", mainPage)
    if len(scdPageUrl) == 0:
        scdPageUrl = re.findall(r"的人.*?a href=\".*?\"", mainPage)
    if len(scdPageUrl) == 0:
        return 0
    scdPageUrl = scdPageUrl[0]
    scdPageUrl = "http://tieba.baidu.com"+re.findall(r"href=\".*?\"", scdPageUrl)[0][6:-1]
    scdPage = getHtml2(scdPageUrl)
    peoplelist = re.findall(r"<a href=\"[^<\"]*?\" target=\"_blank\">[^>]*?</a></span>&nbsp", scdPage)
    lists = []
    for a in peoplelist:
        url = "http://tieba.baidu.com" + re.findall(r"href=\".*?\"", a)[0][6:-1]
        name = re.findall(r">.*?</a>", a)[0][1:-4]
        lists.append((name, url))
    return lists

url = "http://tieba.baidu.com/home/main?ie=utf-8&un=FightingTK&fr=itb"
dc = {"FT":{}}
used_list = []
thread_num = 10

class thread_tieba(threading.Thread):

    def __init__(self, name, id):
        super(thread_tieba,self).__init__()
        self.id = id
        self.loop = 0
        self.url = url

    def spider(self, url, depth, dic):
        list = getPeoples(url)
        if depth == 2:
            return 0
        if list == 0:return 0
        numlist = range(len(list))
        numlist = filter(self.in_th, numlist)
        """
        随机一个编号,直到链表空掉
        """ 
        i = 0
        tmp_list = []
         
        for i in numlist:
            tmp_list.append(list[i])
        #list = tmp_list
        for b in list:
            if b[0] not in used_list:
                used_list.append(b[0])
                dic.setdefault(b[0],{})
                print " "*10*(depth+1)+b[0]+str(self.id)       
                #self.spider(b[1], depth+1, dic[b[0]])  
                self.spider(b[1], depth+1, {})  
  
    def in_th(self, i):
        return i%thread_num == self.id     

    def run(self):
        #while(True):
        print "self.id"+str(self.id)+" run"
        self.spider(url, 0, dc["FT"])    

for i in range(thread_num):
    tt = thread_tieba(str(i), i)
    tt.start()


