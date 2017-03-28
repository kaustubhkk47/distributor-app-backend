from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=3)

    def __str__(self):
        return self.short_name
