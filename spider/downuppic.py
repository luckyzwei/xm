#coding:utf-8

timeout = 5
import requests
import sys
import os
from qcloud_cos import *

qcloud_bucket=u"pic"
qcloud_dirname=u"picf"
downloadtimeout = 10 #下载图片超时10秒
downloadpath = u'./download/'
headers = {"Accept":"image/webp,*/*;q=0.8", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36","Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4","Referer":"http://m.wujiecao.cn/"}

prjpath =  os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'mysite'))
sys.path.append(prjpath+"/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.core.wsgi import get_wsgi_application
from django.conf import settings

application = get_wsgi_application()
from xm.models.models import *

appid = 10073312
secret_id = u'AKIDpeI0azfFGE75zhzZotnV1fDnHc8Wr3GK'
secret_key = u'AF9sT3mOp5A9OZZRn4A5oQrRuCICueFe'
cos_client = CosClient(appid, secret_id, secret_key)


def download_pic(url):
    local_filename = url.split('/')[-1]
    local_path = downloadpath + local_filename
    #首先删除掉
    os.system("rm %s -f" % local_filename)
    try:
        r = requests.get(url, stream=True, timeout=downloadtimeout, headers=headers)
    except BaseException, e:
        msg = "get [%s] error exception:%s" % (url, str(e))
        print msg
        return False,msg,"",""
    if r.status_code != 200:
        msg = "http code is not 200.return:%d" % r.status_code
        return False,msg,"",""
    with open(local_path,'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()
    return True,"",local_path,local_filename

def process_pic_url(url):
    ret,msg,filepath,filename = download_pic(url)
    if ret != True:
        print "process [%s] error.msg:%s" % (url, msg)
        return False,""
    #已经下载到了filepath路径上了，上传到对象存储系统中
    qcloud_filepath = "/%s/%s" % (qcloud_dirname,filename)
    request = UploadFileRequest(qcloud_bucket, qcloud_filepath,filepath)
    obj = cos_client.upload_file(request)
    #删除文件
    os.system('rm %s -f' % filepath)
    if obj["code"]  == 0:
        print "upload [%s] success" % url
        return True,qcloud_filepath
    elif obj["code"] == -4018:
        print "upload [%s] success [already upload]" % url
        return True,qcloud_filepath
    else:
        print "upload [%s] failed.code:%d msg:%s" % (url, obj["code"], obj["message"])
        return False,""

def process_all_imgs():
    itemlist = Itemlist.objects.filter(hasdownpic=0)
    for item in itemlist:
        #下载小图和下载大图
        ret,urlpath = process_pic_url(item.smalllpicurl_old)
        if ret:
            item.smalllpicurl = urlpath
        ret,urlpath = process_pic_url(item.bigpicurl_old)
        if ret:
            item.bigpicurl = urlpath
        item.hasdownpic = 1
        item.save()
        #print("id:%d"%item.id)
if __name__ == "__main__":
    process_all_imgs()

