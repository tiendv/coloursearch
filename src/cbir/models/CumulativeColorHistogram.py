from django.db import models
from .ImageExtraction import ImageExtraction


class CumulativeColorHistogram(models.Model):
    image_extraction = models.ForeignKey(ImageExtraction, on_delete=models.CASCADE)
    ccomponent1_min = models.IntegerField()
    ccomponent1_max = models.IntegerField()
    ccomponent2_min = models.IntegerField()
    ccomponent2_max = models.IntegerField()
    ccomponent3_min = models.IntegerField()
    ccomponent3_max = models.IntegerField()
    value = models.FloatField(null=False, default=0)
