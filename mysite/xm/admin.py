from django.contrib import admin

# Register your models here.

from models.models  import Catalog
from models.models  import Itemlist

admin.site.register(Catalog)
admin.site.register(Itemlist)
