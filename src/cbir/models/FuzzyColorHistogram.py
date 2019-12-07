from django.db import models
from .ImageExtraction import ImageExtraction


class FuzzyColorHistogram(models.Model):
    image_extraction_id = models.IntegerField()
    ccomponent1 = models.FloatField()
    ccomponent2 = models.FloatField()
    ccomponent3 = models.FloatField()
    value = models.FloatField(null=False, default=0)
