from django.db import models


class Directory(models.Model):
    path = models.TextField(max_length=1000)
