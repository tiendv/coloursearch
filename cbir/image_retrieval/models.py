from django.db import models

# Create your models here.


class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    location = models.TextField(max_length=255)
