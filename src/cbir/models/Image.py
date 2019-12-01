from django.db import models


class Image(models.Model):
    location = models.TextField(max_length=255)
