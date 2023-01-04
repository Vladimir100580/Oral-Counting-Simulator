from django.contrib import admin
from .models import DataUser, Indexs


class DataUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'log', 'scores', 'fik', 'scorTD', 'quantwin', 'quanttop', 'pop', 'poptd', 'res1')
    list_display_links = ('log', 'scores')
    search_fields = ('log', 'scores', 'fik')

admin.site.register(DataUser, DataUserAdmin)


class IndexsAdmin(admin.ModelAdmin):
    list_display = ('id', 'log', 'ips', 'ipskol', 'curdate')
    list_display_links = ('id', 'log', 'ips', 'ipskol')
    search_fields = ('log', 'ips')

admin.site.register(Indexs, IndexsAdmin)


