import time
from scripts.utils import get_image_url

def serialize_order(orderItem):
    print orderItem
    order = {
        "orderID": orderItem.order_id,
    }
    return order


def order_parser(orderQuerySet):
    orders = []
    products = []

    for i in range(len(orderQuerySet)):
        orders.append(serialize_order(orderQuerySet[i]))
        #products.append(serialize_order_product(orderQuerySet[i]))
    return orders
