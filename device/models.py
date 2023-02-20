from django.db import models

# Create your models here.
class Device(models.Model):
    id = models.CharField(max_length= 36, primary_key= True)
    name = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)
    version = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

class Device_Sensor(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    sensor = models.ForeignKey('sensor.Sensor', on_delete=models.CASCADE)

class Device_Attribute(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    attribute = models.ForeignKey('attribute.Attribute', on_delete=models.CASCADE)

class Device_Connection(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    connection = models.ForeignKey('connection.Connection', on_delete=models.CASCADE)
