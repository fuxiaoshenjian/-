#!usr/bin/python#coding=utf-8
import threading
import urllib
import sys
from bs4 import BeautifulSoup
import thread
import re
import Queue

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

def getPeoples(mainPage):
    """
    获取所有的关注者的url
    """
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
dc = {"FT":{url:[]}}
used_list = []

def spider(depth, dic_list):
    """
    获取所有的关注者的url
    """
    
    #print "!!层数:"+str(depth)
    for K,W in dic_list.items():
        print " "*depth*5+K
        for k, w in W.items():
            url = k 
        temp_list = getPeoples(getHtml(url))
        print len(temp_list)
        if temp_list == 0:
            return 0
        for b in temp_list:
            if b[0] not in used_list:
                W[url].append({b[0]:{b[1]:[]}})
                used_list.append("b[0]")
        depth += 1
        if depth == 3:
            return 0 
        for a in W[url]:
             #print "开始爬"+str(a)+"的主页"
             spider(depth, a)
        break

    return dic_list

class thread_tieba(threading.Thread):

    def __init__(self, name, id):
        super(thread_tieba,self).__init__()
        self.id = id
        self.loop = 0
        self.url = url

    def run(self):
        print "self.id"+" run"
        spider(0, dc)
#print spider(0, dc)
for i in range(20):
    tt = thread_tieba(str(i), i)
    tt.start()

sys.exit()

