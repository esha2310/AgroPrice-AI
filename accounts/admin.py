from django.contrib import admin
from .models import WatchItem
admin.site.register(WatchItem)
admin.site.site_header='AgroPrice AI Administration'
admin.site.site_title='AgroPrice AI'
admin.site.index_title='Accounts and saved markets'
