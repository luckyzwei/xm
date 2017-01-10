#coding:utf-8
from xm.models.models import *
from xm.utils.utils import *
from django.conf import settings
from django.db.models import Q

# Create your views here.

def ConverOnePicUrl(url):
    return settings.PICURL_PREFEX + url

def ConvertPicUrl(itemlist):
    newlist = []
    for item in itemlist:
        item.picurl = settings.PICURL_PREFEX + item.picurl
        item.bigpicurl = settings.PICURL_PREFEX + item.bigpicurl
        newlist.append(item)
    return newlist
def ConvertItemUrl(itemlist,beginindex):
    newlist = []
    for item in itemlist:
        beginindex = beginindex + 1


        item.smalllpicurl= settings.PICURL_PREFEX + item.smalllpicurl
        item.bigpicurl = settings.PICURL_PREFEX + item.bigpicurl
        item.smalllpicurl_old = ""
        item.bigpicurl_old = beginindex
        item.addtime = None
        item.index = beginindex
        newlist.append(item)

    return newlist

def GetCatalog(request):
    cataloglist = Catalog.objects.all()
    cataloglist = ConvertPicUrl(cataloglist)
    newcataloglist = []
    for catalog in cataloglist:
        if catalog.visibal == 1:
            newcataloglist.append(catalog)
    return JsonResponse({"ret":0,"cataloglist":newcataloglist})

def ConvertDes(des):
    if len(des) > settings.DESNUM:
        return des[0:20] + "..."
    return des


def GetOneCatalog(request):
    page = 1
    try:
        catalogid = int(request.GET["id"])
        page = int(request.GET['page'])
        sort = int(request.GET['sort']) #sort为0表示正序,为1表示倒序
    except:
        return JsonResponse({"ret":-1, "msg":u"请传入正确的参数"})
    try:
        catalogobj = Catalog.objects.get(id = catalogid)
        catalogobj.picurl = settings.PICURL_PREFEX + catalogobj.picurl
        catalogobj.bigpicurl = settings.PICURL_PREFEX + catalogobj.bigpicurl
        catalogobj.description = ConvertDes(catalogobj.description)
    except:
        return JsonResponse({'ret':-1, 'msg':u'找不到对象!'})
    if page < 1:
        page = 1
    flag = "id"
    if sort == 1:
        flag = "-id"
    onepagenum = settings.ONEPAGENUM
    totle_count = Itemlist.objects.filter(catalog=catalogobj).count()
    totle_page = totle_count/onepagenum
    itemlist = Itemlist.objects.filter(catalog=catalogobj).order_by(flag)[(page-1)*onepagenum:page*onepagenum]
    itemlist = ConvertItemUrl(itemlist,(page-1)*onepagenum)
    return JsonResponse({"ret":0,"itemlist":itemlist,"totle_page":totle_page,"catalog":catalogobj})

def GetOneItem(request):
    try:
        itemid = int(request.GET["id"])
    except:
        return JsonResponse({"ret":-1, "msg":u"请传入正确的参数"})
    try:
        itemobj = Itemlist.objects.get(id=itemid)
    except:
        return JsonResponse({"ret":-1,"msg":u'无法找到对象'})
    itemobj.smalllpicurl= settings.PICURL_PREFEX + itemobj.smalllpicurl
    itemobj.bigpicurl = settings.PICURL_PREFEX + itemobj.bigpicurl
    itemobj.smalllpicurl_old = ""
    itemobj.bigpicurl_old = ""
    itemobj.addtime = None

    #找到关联图片
    picobjlist = Piclist.objects.filter(owner=itemobj)
    logger.error("picobjlist size:%d" % len(picobjlist))
    picurllist = []
    for picobj in picobjlist:
        picurllist.append(ConverOnePicUrl(picobj.pic_url))

    #随机寻找条目
    #找到上一章节和下一章节
    israndom = 0
    if itemobj.index < 0:
        randomlist = Itemlist.objects.filter(catalog=itemobj.catalog).order_by('?')[:4]
        randomlist = ConvertItemUrl(randomlist,0)
        israndom = 1
    else:
        randomlist = Itemlist.objects.filter(Q(catalog=itemobj.catalog), Q(index=itemobj.index-1)|Q(index=itemobj.index+1)).order_by("index")
        randomlist = ConvertItemUrl(randomlist,0)

    return JsonResponse({"ret":0,"itemobj":itemobj,"israndom":israndom,"randomlist":randomlist, "picurllist":picurllist})
