from django.contrib import admin

from .models.orders import Order
from .models.orderItems import OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
