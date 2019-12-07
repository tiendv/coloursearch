from django.db import models


class Method(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    detail = models.CharField(max_length=255, unique=True, null=False)
