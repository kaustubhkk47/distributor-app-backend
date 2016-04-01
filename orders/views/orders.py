from django.views.decorators.csrf import csrf_exempt

from ..models.order import Order
from ..models.orderItem import OrderItem

from users.models.distributors import Distributor
from pincodes.models import Pincode

from ..serializers.orders import order_parser
from scripts.utils import customResponse, convert_keys_to_string

import json

def get_orders_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    orders = OrderItem.objects.filter(order__distributor__id=distributorID).select_related()
    return customResponse("2XX", {"orders": order_parser(orders)})

@csrf_exempt
def post_order_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']
    salesmanID = tokenPayload['salesmanID']

    try:
        requestBody = json.loads(request.body.decode("utf-8"))
        requestBody = convert_keys_to_string(requestBody)
        requestOrders = convert_keys_to_string(requestBody['orders'])

        orders = []
        for i in range(len(requestOrders)):
            orders.append(convert_keys_to_string(requestOrders[i]))

        if len(orders) == 0:
            return customResponse("4XX", {"error": "no orders"})
    except Exception as e:
        print e
        errorMessage = {
            "message": "Invalid data sent in request",
        }
        return customResponse("4XX", errorMessage)
    print orders

    responseOrderIDs = []
    for i in range(len(orders)):
        products = convert_keys_to_string(orders[i]['products'])
        retailerID = orders[i]['retailerID']
        totalPrice = orders[i]["totalPrice"]
        editedPrice = orders[i]["editedPrice"]
        productCount = orders[i]["productCount"]

        try:
            orderPtr = Order.objects.create(distributor_id=distributorID, salesman_id=salesmanID, retailer_id=retailerID, totalPrice=totalPrice, editedPrice=editedPrice, productCount=productCount)
        except Exception as e:
            print e
            return customResponse("4XX", {"error": "unable to create order entry"})

        responseOrderIDs.append(orderPtr.id)

        try:
            latestOrderItemID = OrderItem.objects.latest('id').id + 1
        except Exception as ex:
            latestOrderItemID = 1

        orderItemEntries = []
        for i in range(len(products)):
            #orderItemEntries.append(OrderItem(id=latestOrderItemID+i, order_id=order.id, product_id=productIDs[i], quantity=quantities[i]))
            try:
                OrderItem.objects.create(order_id=orderPtr.id, product_id=products[i]['productID'], quantity=products[i]['quantity'])
            except Exception as e:
                print e
                return customResponse("4XX", {"error": products[i]})
        #orderItems = OrderItem.objects.bulk_create(orderItemEntries)
    return customResponse("2XX", {"orderIDs":responseOrderIDs})
