from django.db import models

from .city import City

class Pincode(models.Model):
    city = models.ForeignKey(City, models.CASCADE)
    pincode = models.CharField(max_length=6)
    locality = models.CharField(max_length=100)

    def __str__(self):
        return self.pincode

    
