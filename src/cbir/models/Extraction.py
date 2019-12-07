from datetime import datetime
from django.db import models
from .Method import Method


class Extraction(models.Model):
    directory_path = models.CharField(max_length=1000)
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now(), null=True)
    end_time = models.DateTimeField(null=True)
    param1_name = models.CharField(max_length=255, null=True)
    param1_value = models.FloatField(null=True)
    param2_name = models.CharField(max_length=255, null=True)
    param2_value = models.FloatField(null=True)
    param3_name = models.CharField(max_length=255, null=True)
    param3_value = models.FloatField(null=True)
