from django.db import models
from .ImageExtraction import ImageExtraction
from .FuzzyColorHistogramColor import FuzzyColorHistogramColor


class FuzzyColorHistogram(models.Model):
    image_extraction = models.ForeignKey(ImageExtraction, on_delete=models.CASCADE)
    color = models.ForeignKey(FuzzyColorHistogramColor, on_delete=models.CASCADE)
    value = models.FloatField(null=False, default=0)
