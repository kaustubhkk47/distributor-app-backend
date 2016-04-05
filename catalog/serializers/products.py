
import time

def serialize_product(productItem):
    product = {
        "productID": productItem.id,
        "distributorID": productItem.distributor_id,
        "name": productItem.name,
        #"unit": productItem.unit,
        "price_per_unit": productItem.price_per_unit,
        "created_at": time.mktime(productItem.created_at.timetuple())*1000,
        "updated_at": time.mktime(productItem.updated_at.timetuple())*1000
    }
    return product


def products_parser(productQuerySet):
    products = []

    for i in range(len(productQuerySet)):
        products.append(serialize_product(productQuerySet[i]))

    return products
