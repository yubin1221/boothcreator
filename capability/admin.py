from django.contrib import admin

# Register your models here.

from .models import Capability,Capability_Data
admin.site.register(Capability)
admin.site.register(Capability_Data)