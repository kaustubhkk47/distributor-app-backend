from django.db import models

from .order import Order
from catalog.models.products import Product

class OrderItem(models.Model):

    order = models.ForeignKey(Order, models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
