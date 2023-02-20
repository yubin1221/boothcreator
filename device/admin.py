from django.contrib import admin

# Register your models here.
from .models import Device,Device_Attribute,Device_Connection,Device_Sensor
admin.site.register(Device)
admin.site.register(Device_Connection)
admin.site.register(Device_Sensor)
admin.site.register(Device_Attribute)