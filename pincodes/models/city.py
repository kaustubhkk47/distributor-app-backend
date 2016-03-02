from django.db import models

from .state import State

class City(models.Model):
    state = models.ForeignKey(State, models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
