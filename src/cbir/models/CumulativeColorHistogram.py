from django.db import models
from .Extraction import Extraction


class CumulativeColorHistogram(models.Model):
    extraction = models.ForeignKey(Extraction, on_delete=models.CASCADE)
    ccomponent1_min = models.IntegerField()
    ccomponent1_max = models.IntegerField()
    ccomponent2_min = models.IntegerField()
    ccomponent2_max = models.IntegerField()
    ccomponent3_min = models.IntegerField()
    ccomponent3_max = models.IntegerField()
    value = models.FloatField(null=False, default=0)
