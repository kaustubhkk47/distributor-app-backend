
from django.db import models

from users.models.distributors import Distributor
from users.models.salesman import Salesman
from users.models.retailers import Retailer

class Order(models.Model):

    distributor = models.ForeignKey(Distributor, models.SET_NULL, blank=True, null=True)
    salesman = models.ForeignKey(Salesman, models.SET_NULL, blank=True, null=True)
    retailer = models.ForeignKey(Retailer, models.SET_NULL, blank=True, null=True)

    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    editedPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    productCount = models.IntegerField(default=0)

    orderOffer = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.distributor.company_name
