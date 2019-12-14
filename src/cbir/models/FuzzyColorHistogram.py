from django.db import models
from .ImageExtraction import ImageExtraction


class FuzzyColorHistogram(models.Model):
    image_extraction_id = models.IntegerField()
    color_id = models.IntegerField()
    value = models.FloatField(null=False, default=0)
