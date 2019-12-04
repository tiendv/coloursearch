from django.db import models
from .Directory import Directory


class Image(models.Model):
    name_with_extension = models.TextField(max_length=1000)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
