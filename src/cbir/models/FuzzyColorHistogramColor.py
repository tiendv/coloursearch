from django.db import models


class FuzzyColorHistogramColor(models.Model):
    number_of_fine_colors = models.IntegerField()
    number_of_coarse_colors = models.IntegerField()
    ccomponent1 = models.FloatField()
    ccomponent2 = models.FloatField()
    ccomponent3 = models.FloatField()
