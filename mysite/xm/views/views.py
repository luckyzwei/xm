from xm.models.models import *
from xm.utils.utils import *
from django.conf import settings

# Create your views here.

def GetCatalog(request):
    cataloglist = Catalog.objects.all()
    return JsonResponse({"ret":0,"cataloglist":cataloglist})


def GetOneCatalog(request):
    page = 1
    try:
        catalogid = request.GET["id"]
        page = int(request.GET['page'])
    except:
        return JsonResponse({"ret":-1, "msg":u"请传入正确的参数"})
    try:
        catalogobj = Catalog.objects.get(id = catalogid)
    except:
        return JsonResponse({'ret':-1, 'msg':u'找不到对象!'})
    if page < 1:
        page = 1
    onepagenum = settings.ONEPAGENUM
    totle_count = Itemlist.objects.filter(catalog=catalogobj).count()
    totle_page = totle_count/onepagenum
    itemlist = Itemlist.objects.filter(catalog=catalogobj).order_by("id")[(page-1)*onepagenum, page*onepagenum]
    return JsonResponse({"ret":0,"itemlist":itemlist,"totle_page":totle_page})

def GetOneItem(request):
    try:
        itemid = request.GET["id"]
    except:
        return JsonResponse({"ret":-1, "msg":u"请传入正确的参数"})
    try:
        itemobj = Itemlist.objects.get(id=itemid)
    except:
        return JsonResponse({"ret":-1,"msg":u'无法找到对象'})
    return JsonResponse({"ret":0,"itemobj":itemobj})
