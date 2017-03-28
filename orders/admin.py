from django.contrib import admin

from .models.order import Order
from .models.orderItem import OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
