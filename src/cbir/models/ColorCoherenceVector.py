from django.db import models
from .ValueType import ValueType
from .Image import Image


class ColorCoherenceVector(models.Model):
    name = models.CharField(max_length=255, null=False, default='')
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    value_type = models.ForeignKey(ValueType, on_delete=models.CASCADE)
    value = models.FloatField(null=False, default=0)
