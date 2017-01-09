#coding:utf-8
#用于图片迁移，后面无用
import os,sys
prjpath =  os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'mysite'))
sys.path.append(prjpath+"/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.core.wsgi import get_wsgi_application
from django.conf import settings

application = get_wsgi_application()
from xm.models.models import *


def moveallpic():
    itemlist = Itemlist.objects.filter(index = -2)
    for item in itemlist:
        print("catalog:%s itemtitle:%s" % (item.catalog.zh_name, item.title))
        picobjlist = Piclist.objects.filter(owner=item)
        if len(picobjlist) != 0:
            for picobj in picobjlist:
                picobj.delete()
                #print("delete one")
        picobj = Piclist(owner=item,index=1,pic_url_old = item.bigpicurl_old, pic_url=item.bigpicurl, hasdownpic=1)
        picobj.save()
        item.index=-3
        item.save()
        #return

    print("all pic is:%d" % len(itemlist))

if __name__ == '__main__':
    print "settings.pagenum:%d" % settings.ONEPAGENUM
    moveallpic()
