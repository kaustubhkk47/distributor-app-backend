from django.views.decorators.csrf import csrf_exempt

from ..models.products import Product

from ..serializers.products import products_parser

from scripts.utils import customResponse, convert_keys_to_string, closeDBConnection

import json

def get_product_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    products = Product.objects.filter(distributor__id=distributorID)
    closeDBConnection()
    return customResponse("2XX", {"products": products_parser(products)})

@csrf_exempt
def post_new_product(request, tokenPayload):
    distributorID = tokenPayload["distributorID"]

    try:
        product = json.loads(request.body.decode("utf-8"))
        product = convert_keys_to_string(product)
    except Exception as e:
        errorMesssage = {
            "error": "Invalid data sent in request",
            "data": json.dumps(product)
        }
        return customResponse("4XX", errorMesssage)

    if not len(product) or not 'name' in product or not 'price_per_unit' in product:
        errorMesssage = {
            "error": "Invalid data sent in request",
            "data": json.dumps(product)
        }
        return customResponse("4XX", errorMesssage)

    try:
        newProduct = Product.objects.create(distributor_id=distributorID, name=product['name'], price_per_unit=product['price_per_unit'])
    except Exception as e:
        closeDBConnection()
        return customResponse("4XX", {"error": "unable to create entry in db"})
    else:
        closeDBConnection()
        return customResponse("2XX", {"product": products_parser([newProduct])})

@csrf_exempt
def update_product_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        product = json.loads(request.body.decode("utf-8"))
        product = convert_keys_to_string(product)
    except Exception as ex:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    if 'productID' not in product:
        return customResponse("4XX", {"error": "productID not present"})

    productPtr = Product.objects.filter(id=int(product['productID']), distributor__id=distributorID)
    productPtr = productPtr[0]

    try:
        if 'name' in product:
            productPtr.name = product['name']
        if 'price_per_unit' in product:
            productPtr.price_per_unit = product['price_per_unit']
        productPtr.save()

    except Exception as e:
        closeDBConnection()
        return customResponse("4XX", {"error": "could not update"})
    else:
        closeDBConnection()
        return customResponse("2XX", {"product": products_parser([productPtr])})

@csrf_exempt
def delete_product(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        product = json.loads(request.body.decode("utf-8"))
        product = convert_keys_to_string(product)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    if not 'productID' in product:
        return customResponse("4XX", {"error": "Invaild data for product sent"})

    try:
        productPtr = Product.objects.get(id=int(product["productID"]))
    except Product.DoesNotExist:
        closeDBConnection()
        return customResponse("4XX", {"error": "No such product exists"})

    if productPtr.distributor_id != distributorID:
        return customResponse("4XX", {"error": "different distributors"})

    productPtr.delete()
    closeDBConnection()
    return customResponse("2XX", {"retailer": products_parser([productPtr])})
