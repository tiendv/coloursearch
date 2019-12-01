from django.db import models


class Method(models.Model):
    name = models.CharField(max_length=255, null=False, default='', unique=True)
