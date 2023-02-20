from django.db import models

# Create your models here.

class Sensor(models.Model):
    id = models.CharField(max_length= 36, primary_key= True)
    name = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)
    version = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

class Sensor_Capability(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    capability = models.ForeignKey('capability.Capability', on_delete=models.CASCADE)