from django.db import models

# Create your models here.
class Attribute(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    key = models.CharField(max_length=50)
    super_permission = models.IntegerField()
    user_permission = models.IntegerField()
    is_object = models.BooleanField()
    is_array = models.BooleanField()
    is_object_array = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Attribute_Data(models.Model):
    models.ForeignKey(Attribute, on_delete=models.CASCADE)
    models.ForeignKey('data.Data', on_delete=models.CASCADE)