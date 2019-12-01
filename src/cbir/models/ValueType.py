from django.db import models
from .Method import Method


class ValueType(models.Model):
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    method_index = models.IntegerField(unique=True)
    description = models.CharField(max_length=255)
