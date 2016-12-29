#coding=utf-8

import os,sys
import requests
from bs4 import BeautifulSoup

timeout = 5 #超时记为5秒
headers = {"Host":"m.wujiecao.cn", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Accept-Encoding":"gzip, deflate, sdch","Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4","Refere":"http://m.wujiecao.cn/xieemanhua","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
allpageurl = {
        "xm":u"http://m.wujiecao.cn/xieemanhua/list_1_%d.html",
    "sexiaojie":u"http://m.wujiecao.cn/sexijuntuan/list_2_%d.html"}

prjpath =  os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'mysite'))
sys.path.append(prjpath+"/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.core.wsgi import get_wsgi_application
from django.conf import settings

application = get_wsgi_application()
from xm.models.models import *

def getonepage(title,pageindex):
    if title not in allpageurl:
        msg = "not find title:%s" % title
        print msg
        return False, msg
    url = allpageurl[title] % pageindex
    print "process url:[%s]" % url
    try:
        r = requests.get(url, timeout=timeout, headers=headers)
    except Exception as e:
        msg = "get [%s] error exception:%s" % (url,str(e))
        print msg
        return False, msg
    if r.status_code != 200:
        msg = "http code is not 200. return:%d" % r.status_code
        return False,msg
    #print r.encoding
    r.encoding = "utf-8"
    #print r.text
    soup = BeautifulSoup(r.text,"html.parser")
    divmain = soup.find('div',id="main")
    if not divmain:
        msg = "not find class=main's div "
        return False,msg
    #print divmain
    lilist = divmain.ul.find_all('li')
    for item in lilist:
        print item.find('a')
        oneurl = item.find('a')['href']
        longname = item.find('a')['title']
        smallpicurl = item.a.img['lazysrc']
        shortname = item.a.find('span', class_="bt").text
        #print(u"我爱你".encode("utf-8"))
        #print("type(shorname):%s" % type(shortname))
        #print(u"shortname:%s" % shortname)
        #print(shortname.encode("utf-8"))
        getdetail(title,oneurl,longname,smallpicurl,shortname)

def getdetail(title,oneurl, longname,smallpicurl, shortname):
    #print(u"oneurl:[%s] longname:[%s] smallpicurl:[%s] shortname:[%s]" % (oneurl, longname, smallpicurl,shortname)).encode('utf-8')
    oneurl = "http://m.wujiecao.cn/%s" % oneurl
    try:
        r = requests.get(oneurl, timeout=timeout, headers=headers)
    except Exception as e:
        msg = "get [%s] error exception:%s" % (oneurl, str(e))
        print msg
        return False,msg
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text,"html.parser")
    divmain = soup.find('div',id="imgString")
    if not divmain:
        msg = "not find class=main's div"
        return False,msg
    imgurl = divmain.img["src"]
    print(u"bigimg:%s" % imgurl)
    itemlist  = Itemlist.objects.filter(title=shortname)
    if len(itemlist) > 0:
        #已经存在了，所以不添加
        print("has exist")
        return
    try:
        catalogobj = Catalog.objects.get(name=title)
    except:
        print("not find catalog:%s" % title)
        return
    itemobj = Itemlist(title=shortname, smalllpicurl_old=smallpicurl, bigpicurl_old=imgurl,catalog=catalogobj)
    itemobj.save()

def addcatalog(name):
    objlist = Catalog.objects.filter(name=name)
    if len(objlist) != 0:
        return
    obj = Catalog(name=name)
    obj.save()

if __name__ == '__main__':
    print "settings.pagenum:%d" % settings.ONEPAGENUM

    #邪恶漫画
    #addcatalog('xm')
    #for i in range(1,87):
    #    getonepage('xm',i)
    addcatalog('sexiaojie')
    for i in range(1,30):
        getonepage('sexiaojie',i)
