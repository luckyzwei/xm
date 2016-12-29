#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Catalog(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        db_table = u'catalog'
        app_label = u'xm'
    def __unicode__(self):
        return u"title"

class Itemlist(models.Model):
    title = models.CharField(max_length=50, unique=True)
    smalllpicurl = models.CharField(max_length=100)
    bigpicurl = models.CharField(max_length=100)
    addtime = models.DateTimeField(default=timezone.now())
    catalog = models.ForeignKey(Catalog)
    class Meta:
        db_table = u'itemlist'
        app_label = u'xm'
    def __unicode__(self):
        return u'title'
