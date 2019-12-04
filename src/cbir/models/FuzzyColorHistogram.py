from django.db import models
from .Extraction import Extraction


class FuzzyColorHistogram(models.Model):
    extraction = models.ForeignKey(Extraction, on_delete=models.CASCADE)
    ccomponent1 = models.IntegerField()
    ccomponent2 = models.IntegerField()
    ccomponent3 = models.IntegerField()
    value = models.FloatField(null=False, default=0)
