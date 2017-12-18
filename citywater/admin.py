from django.contrib import admin

# Register your models here.
from .models import City, District, Water

admin.site.register(City)
admin.site.register(District)

class WaterAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'date', 'available', )

admin.site.register(Water, WaterAdmin)
