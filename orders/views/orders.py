from django.views.decorators.csrf import csrf_exempt

from ..models.order import Order
from ..models.orderItem import OrderItem

from catalog.models.offers import *
from catalog.serializers.offers import *
from users.models.distributors import Distributor
from pincodes.models import Pincode

from ..serializers.orders import order_parser
from scripts.utils import customResponse, convert_keys_to_string, closeDBConnection

import json, time

def get_orders_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    orders = []
    ordersPtr = Order.objects.filter(distributor__id=distributorID).select_related()
    for i in range(len(ordersPtr)):
        order = {
            "orderID": ordersPtr[i].id,
            "distributorID": ordersPtr[i].distributor_id,
            "productCount": ordersPtr[i].productCount,
            "totalPrice": ordersPtr[i].totalPrice,
            "editedPrice": ordersPtr[i].editedPrice,
            "orderOffer": [],
            "created_at": time.mktime(ordersPtr[i].created_at.timetuple())*1000,
            "updated_at": time.mktime(ordersPtr[i].updated_at.timetuple())*1000
        }

        if ordersPtr[i].orderOffer:
            orderOffer = [int(e) if e.isdigit() else e for e in ordersPtr[i].orderOffer.split(",")]
            orderOfferPtr = OrderOffer.objects.filter(id__in=orderOffer)

            order["orderOffer"] = orderOffers_parser(orderOfferPtr)

        try:
            order["retailer"]= {
                "retailerID": ordersPtr[i].retailer_id,
                "company_name": ordersPtr[i].retailer.company_name
            }
        except Exception as e:
            order["retailer"]= {
                "retailerID": None,
                "company_name": None
            }

        try:
            order["salesman"] = {
                "salesmanID": ordersPtr[i].salesman_id,
                "name": ordersPtr[i].salesman.name
            }
        except Exception as e:
            order["salesman"] = {
                "salesmanID": None,
                "name": None
            }

        orderItemPtr = OrderItem.objects.filter(order__id=ordersPtr[i].id)
        products = []
        for j in range(len(orderItemPtr)):
            try:
                product = {
                    "productID": orderItemPtr[j].product_id,
                    "name": orderItemPtr[j].product.name,
                    "quantity": orderItemPtr[j].quantity,
                    "price_per_unit": orderItemPtr[j].product.price_per_unit,
                    "productOffer": []
                }

                if orderItemPtr[j].productOffer:
                    productOffer = [int(e) if e.isdigit() else e for e in orderItemPtr[j].productOffer.split(',')]
                    productOfferPtr = ProductOffer.objects.filter(id__in=productOffer).select_related()

                    product["productOffer"] = productOffers_parser(productOfferPtr)

            except Exception as e:
                product = {
                    "productID": orderItemPtr[j].product_id,
                    "name": None,
                    "quantity": orderItemPtr[j].quantity,
                    "price_per_unit": None,
                    "productOffer": []
                }

            products.append(product)
        order["products"] = products

        orders.append(order)
    closeDBConnection()
    return customResponse("2XX", {"orders": orders})

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
        errorMessage = {
            "message": "Invalid data sent in request",
        }
        return customResponse("4XX", errorMessage)

    responseOrderIDs = []
    for i in range(len(orders)):

        products = convert_keys_to_string(orders[i]['products'])
        retailerID = orders[i]['retailerID']
        totalPrice = orders[i]["totalPrice"]
        editedPrice = orders[i]["editedPrice"]
        productCount = orders[i]["productCount"]

        orderOffer = ",".join(map(str, orders[i]["orderOffer"])) if "orderOffer" in orders[i] else ""
        print orderOffer
        try:
            orderPtr = Order.objects.create(distributor_id=distributorID, salesman_id=salesmanID, retailer_id=retailerID, totalPrice=totalPrice, editedPrice=editedPrice, productCount=productCount, orderOffer=orderOffer)
        except Exception as e:
            closeDBConnection()
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
                productOffer = ",".join(map(str, products[i]["productOffer"])) if "productOffer" in products[i] else ""
                OrderItem.objects.create(order_id=orderPtr.id, product_id=products[i]['productID'], quantity=products[i]['quantity'], productOffer=productOffer, freeQuantity=products[i]["freeQuantity"])
            except Exception as e:
                return customResponse("4XX", {"error": products[i]})
        #orderItems = OrderItem.objects.bulk_create(orderItemEntries)
    closeDBConnection()
    return customResponse("2XX", {"orderIDs":responseOrderIDs})
