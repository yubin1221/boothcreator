import uuid

from django.db import models


# Create your models here.
class Data(models.Model):
    DATA_TYPE = [
        ('integer', 'integer'),
        ('string', 'string'),
        ('number', 'number'),
        ('boolean', 'boolean')
    ]
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4())
    name = models.CharField(max_length=50)
    primitive = models.CharField(max_length=7, choices=DATA_TYPE)

    is_category = models.BooleanField()
    has_length_limit = models.BooleanField(null=True)
    has_range_limit = models.BooleanField(null=True)
    default_value = models.TextField(null=True)
    unit_of_value = models.CharField(max_length=10)
    min_length = models.IntegerField(null=True)
    max_length= models.IntegerField(null=True)
    format = models.TextField(null=True)
    pattern = models.TextField(null=True)
    minimum = models.BigIntegerField(null=True)
    maximum = models.BigIntegerField(null=True)
    multiple_of = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
