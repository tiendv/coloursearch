from django.db import models
from .ImageExtraction import ImageExtraction


class ColorCoherenceVector(models.Model):
    image_extraction = models.ForeignKey(ImageExtraction, on_delete=models.CASCADE)
    ccomponent1 = models.IntegerField()
    ccomponent2 = models.IntegerField()
    ccomponent3 = models.IntegerField()
    alpha = models.IntegerField(null=False, default=0)
    beta = models.IntegerField(null=False, default=0)

