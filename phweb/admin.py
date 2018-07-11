from django.contrib import admin
from phweb.models import Deg, Ph, Redox, Piscine, Battery
# Register your models here.

class DegAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'celsius', 'user')

admin.site.register(Deg, DegAdmin)

class PhAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'phval', 'user')

admin.site.register(Ph, PhAdmin)

class RedoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'redoxval', 'user')

admin.site.register(Redox, RedoxAdmin)

class PiscineAdmin(admin.ModelAdmin):
    list_display = ('id', 'capacity', 'user', 'enable_shutdown', 'do_update')

admin.site.register(Piscine, PiscineAdmin)


class BatteryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'battery_charge')

admin.site.register(Battery, BatteryAdmin)

