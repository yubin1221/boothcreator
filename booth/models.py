from django.db import models

# Create your models here.
class Booth(models.Model):
    id = models.CharField(max_length= 36, primary_key= True)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)


class Booth_Device(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    device = models.ForeignKey('device.Device', on_delete=models.CASCADE)

