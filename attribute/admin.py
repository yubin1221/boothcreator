from django.contrib import admin

# Register your models here.
from .models import Attribute,Attribute_Data
# Register your models here.
admin.site.register(Attribute)
admin.site.register(Attribute_Data)
