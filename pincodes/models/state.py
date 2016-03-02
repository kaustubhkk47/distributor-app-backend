from django.db import models

from .country import Country

class State(models.Model):
    country = models.ForeignKey(Country, models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
