from django.views.decorators.csrf import csrf_exempt

from ..models.order import Order
from ..models.orderItem import OrderItem

from users.models.distributors import Distributor
from pincodes.models import Pincode

from ..serializers.orders import order_parser
from scripts.utils import customResponse

import json

def get_orders_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    orders = OrderItem.objects.filter(order__distributor__id=distributorID).select_related()
    return customResponse("2XX", {"orders": order_parser(orders)})
