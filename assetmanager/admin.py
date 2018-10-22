from django.contrib import admin

from .models import Asset, Location, Count

# Register your models here.
admin.site.register(Asset)
admin.site.register(Location)
admin.site.register(Count)