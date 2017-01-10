#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Catalog(models.Model):
    name = models.CharField(max_length=50, unique=True)
    zh_name = models.CharField(max_length=50, default="")
    picurl = models.CharField(max_length=200, default="")
    parent_name = models.CharField(max_length=256, default="") #父级目录
    visibal = models.IntegerField(default=1); #默认可见
    bigpicurl = models.CharField(max_length=256, default="")
    description = models.CharField(max_length=256, default="")
    class Meta:
        db_table = u'catalog'
        app_label = u'xm'
    def __unicode__(self):
        return u"%s" % self.name

#这里的id就是意味着第几话
class Itemlist(models.Model):
    title = models.CharField(max_length=50)
    smalllpicurl = models.CharField(max_length=100,default="")
    bigpicurl = models.CharField(max_length=100,default="")
    addtime = models.DateTimeField(default=timezone.now())
    catalog = models.ForeignKey(Catalog)
    hasdownpic = models.IntegerField(default=0)
    smalllpicurl_old = models.CharField(max_length=256,default="")
    bigpicurl_old = models.CharField(max_length=256,default="")
    url_old = models.CharField(max_length=256,default="")
    index = models.IntegerField(default = -1) #指明是多少话
    class Meta:
        db_table = u'itemlist'
        app_label = u'xm'
    def __unicode__(self):
        return u'%s' % self.title

class Piclist(models.Model):
    index = models.IntegerField() #此为在一话中的图片顺序
    pic_url_old = models.CharField(max_length = 256)
    pic_url = models.CharField(max_length=256)
    hasdownpic = models.IntegerField(default = 0)
    owner = models.ForeignKey(Itemlist)
    class Meta:
        db_table = u"piclist"
        app_label = u'xm'
    def __unicode__(self):
        return u'%s_%d' % (self.owner.title, self.index)
