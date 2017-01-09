from django.contrib import admin

# Register your models here.

from models.models  import Catalog
from models.models  import Itemlist
from models.models  import Piclist

admin.site.register(Catalog)
admin.site.register(Itemlist)
admin.site.register(Piclist)
