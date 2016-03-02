from django.db import models

from .products import Product

class Offer(models.Model):

    product = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True)

    title = models.CharField(max_length=200, blank=True, null=False)
    offer_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
