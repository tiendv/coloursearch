from django.db import models
from ..models import Extraction


class ImageExtraction(models.Model):
    extraction = models.ForeignKey(Extraction, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=1000)
    thumbnail_path = models.CharField(max_length=1000)
