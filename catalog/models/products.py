
from django.db import models

from users.models.distributors import Distributor

class Product(models.Model):

    distributor = models.ForeignKey(Distributor, models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=200, blank=False)
    unit = models.CharField(max_length=15, blank=True, null=False)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
