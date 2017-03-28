from django.db import models

from .order import Order
from catalog.models.products import Product

class OrderItem(models.Model):

    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)

    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    editedPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    productOffer = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=False)
    freeQuantity = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return "Product: " + self.product.name + ', quantity: ' + self.quantity
