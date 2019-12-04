from django.db import models
from .Extraction import Extraction


class ColorCoherenceVector(models.Model):
    extraction = models.ForeignKey(Extraction, on_delete=models.CASCADE)
    ccomponent1 = models.IntegerField()
    ccomponent2 = models.IntegerField()
    ccomponent3 = models.IntegerField()
    alpha = models.IntegerField(null=False, default=0)
    beta = models.IntegerField(null=False, default=0)

