#coding=utf-8
import os,sys
import requests
from bs4 import BeautifulSoup
prjpath =  os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'mysite'))
sys.path.append(prjpath+"/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.core.wsgi import get_wsgi_application
from django.conf import settings
application = get_wsgi_application()
from xm.models.models import *


timeout = 10 #超时记为5秒
print ("settings:%d" % (settings.ONEPAGENUM))
headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding":"gzip, deflate, sdch", "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4","Host":"www.quhua.com","Referer":"http://www.quhua.com/","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
urlprefix = "http://www.quhua.com"

#获取漫画列表,传入漫画页面
def getmhlist(url,parentname):
    try:
        r = requests.get(url,timeout = timeout, headers=headers)
    except Exception as e:
        msg = "get [%s] error exception:%s" % (url, str(e))
        print msg
        return False, msg
    if r.status_code != 200:
        msg = "http code is not 200. return :%d" % r.status_code
        return False,msg

    #print r.encoding
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    alla = soup.find_all("a", class_="card_item")
    for item in alla:
        name = item.find('img')['alt']
        smallpicurl = item.find('img')['src']
        itemurl = urlprefix + item["href"]

        cataloglist = Catalog.objects.filter(name=name)
        if len(cataloglist) == 0 :
            catalog = Catalog(name=name,zh_name=name,picurl=smallpicurl,parent_name = parentname)
            catalog.save()
        else:
            catalog = cataloglist[0]
        getonemh(itemurl,catalog)
        print "name:%s smallpicurl:%s itemurl:%s" % ( name, smallpicurl, itemurl )

#得到一个漫画目录
def getonemh(url, catalog):
    try:
        r = requests.get(url, timeout= timeout, headers=headers)
    except Exception as e:
        msg = "get [%s] error exception:%s" % (url, str(e))
        print msg
        return False, msg
    if r.status_code != 200:
        msg = "http code is not 200. return :%d" % r.status_code
        return False,msg
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    divmain = soup.find('div',class_="detail_lst")
    if not divmain:
        msg = 'not find class="detail_lst"'
        print msg
        return False,msg
    lilist = divmain.ul.find_all('li')
    for item in lilist:
        oneurl = urlprefix + item.a['href']
        smallpic =  item.a.img['src']
        hua = item.a.img['alt'].split(' ')[0].replace(u'第','').replace(u'话','').replace(u'部','').replace(u'话','').replace(u'季','').replace(u'[','').replace(u']','')
        name = item.a.find(class_="subj").span.text
        huaint = 0
        if not hua.isdigit():
            print("isnotdigit.....")
            print(u"%s index:%s"%(name, hua))
            huaint = 0
        else:
            huaint = int(hua)
        #print(u"%s index:%s"%(name, hua))
        getoneiteminmh(oneurl, huaint, smallpic, name,catalog)

#得到一个漫画的一个子项目
def getoneiteminmh(url, huashu, smallpic, title, catalog):
    try:
        r = requests.get(url, timeout=timeout, headers=headers)
    except Exception as e:
        msg = "get [%s] error exception:%s" % (url, str(e))
        print msg
        return False, msg
    if r.status_code != 200:
        msg = "http code is not 200. return :%d" % r.status_code
        return False,msg
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    imglist = soup.find_all('img', class_='_images')
    #首先增加一个item，然后一条一条的图片往里面加
    olditemlist = Itemlist.objects.filter(title=title, catalog=catalog)
    if len(olditemlist) > 0:
        itemobj = olditemlist[0]
    else:
        itemobj = Itemlist(title=title,smalllpicurl_old = smallpic, catalog=catalog, url_old=url, index=huashu)
        itemobj.save()
    index = 1
    for imgitem in imglist:
        imgsrc = imgitem['src']
        print("index:%d url:%s" % (index, imgsrc))
        piclist = Piclist.objects.filter(owner=itemobj)
        if len(piclist) > 0:
            picobj = piclist[0]
            picobj.delete()
        picobj = Piclist(index=index, pic_url_old=imgsrc, owner=itemobj)
        picobj.save()
        index += 1

if __name__ == '__main__':
    url = u"http://www.quhua.com/gaoxiao/"
    getmhlist(url,"gaoxiao")
    print "beign..."
