from django.contrib import admin

# Register your models here.
from .models import Booth,Booth_Device
admin.site.register(Booth)
admin.site.register(Booth_Device)