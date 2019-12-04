from datetime import datetime
from django.db import models
from .Image import Image
from .Method import Method


class Extraction(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now(), blank=True)
    param1_name = models.CharField(max_length=255,)
    param1_value = models.FloatField()
    param2_name = models.CharField(max_length=255)
    param2_value = models.FloatField()
    param3_name = models.CharField(max_length=255)
    param3_value = models.FloatField()
