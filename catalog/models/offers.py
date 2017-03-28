from django.db import models

from .products import Product
from users.models.distributors import Distributor

class Offer(models.Model):

    distributor = models.ForeignKey(Distributor, models.SET_NULL, blank=True, null=True)

    title = models.CharField(max_length=200, blank=False, null=False)
    offer_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class OfferType(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name

class OrderOffer(models.Model):
    distributor = models.ForeignKey(Distributor, models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=200, blank=False, null=True)
    discount = models.DecimalField(max_digits=6, decimal_places=2, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductOffer(models.Model):

    product = models.ForeignKey(Product)
    # offerType = models.PositiveIntegerField(blank=False, null=False)
    offerType = models.ForeignKey(OfferType)
    description = models.TextField(blank=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
