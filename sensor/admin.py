from django.contrib import admin

# Register your models here.

from .models import Sensor,Sensor_Capability
admin.site.register(Sensor)
admin.site.register(Sensor_Capability)
