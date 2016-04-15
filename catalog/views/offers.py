from django.views.decorators.csrf import csrf_exempt
from ..models.offers import *

from ..serializers.offers import offers_parser, orderOffers_parser, productOffers_parser

from scripts.utils import customResponse, convert_keys_to_string, closeDBConnection
import json

def get_offer_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    orderOffers = OrderOffer.objects.filter(distributor__id=distributorID)
    productOffers = ProductOffer.objects.filter(product__distributor__id=distributorID)

    response = {
        "orderOffers": orderOffers_parser(orderOffers),
        "productOffers": productOffers_parser(productOffers)
    }
    closeDBConnection()
    return customResponse("2XX", {"offers": response})

def get_offer_types_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    offerTypes = OfferType.objects.all()

    response = []
    for i in range(len(offerTypes)):
        response.append({
            "offerTypeID": offerTypes[i].id,
            "offerTypeName": offerTypes[i].name,
        })

    closeDBConnection()
    return customResponse("2XX", {"offerTypes": response})

@csrf_exempt
def post_new_order_offer_details(request, tokenPayload):
    distributorID = tokenPayload["distributorID"]

    try:
        orderOffer = json.loads(request.body.decode("utf-8"))
        orderOffer = convert_keys_to_string(orderOffer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    if not len(orderOffer):
        return customResponse("4XX", {"error": "Invaild data for offer sent"})

    try:
        newOrderOffer = OrderOffer.objects.create(distributor_id=distributorID, name=orderOffer['name'], discount=orderOffer["discount"])

    except Exception as e:
        closeDBConnection()
        return customResponse("4XX", {"error": "unable to create entry in db"})

    closeDBConnection()
    return customResponse("2XX", {"orderOffer": orderOffers_parser([newOrderOffer])})

@csrf_exempt
def delete_order_offer_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        orderOffer = json.loads(request.body.decode("utf-8"))
        orderOffer = convert_keys_to_string(orderOffer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    if not 'orderOfferID' in orderOffer:
        return customResponse("4XX", {"error": "Invaild data for offer sent"})

    try:
        orderOfferPtr = OrderOffer.objects.get(id=int(orderOffer["orderOfferID"]))
    except OrderOffer.DoesNotExist:
        closeDBConnection()
        return customResponse("4XX", {"error": "No such Offer exists"})

    if orderOfferPtr.distributor_id != distributorID:
        return customResponse("4XX", {"error": "different distributor"})

    orderOfferPtr.delete()
    closeDBConnection()
    return customResponse("2XX", {"orderOffer": orderOffers_parser([orderOfferPtr])})

@csrf_exempt
def update_order_offer_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        orderOffer = json.loads(request.body.decode("utf-8"))
        orderOffer = convert_keys_to_string(orderOffer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    if not len(orderOffer):
        return customResponse("4XX", {"error": "Invaild data for offer sent"})

    orderOfferPtr = OrderOffer.objects.filter(id=orderOffer["orderOfferID"], distributor__id=distributorID)
    if len(orderOfferPtr) == 0:
        closeDBConnection()
        return customResponse("4XX", {"error": "No such offer exists"})

    orderOfferPtr = orderOfferPtr[0]

    try:
        orderOfferPtr.name = orderOffer['name']
        orderOfferPtr.discount = orderOffer['discount']

        orderOfferPtr.save()
        closeDBConnection()
    except Exception as e:
        closeDBConnection()
        return customResponse("4XX", {"error": "could not update"})
    else:
        return customResponse("2XX", {"offer": orderOffers_parser([orderOfferPtr])})

@csrf_exempt
def post_new_product_offer_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        productOffer = json.loads(request.body.decode("utf-8"))
        productOffer = convert_keys_to_string(productOffer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    if not len(productOffer):
        return customResponse("4XX", {"error": "Invaild data for product offer sent"})

    productOffer["description"] = json.dumps(convert_keys_to_string(productOffer["description"]))
    try:
        productOfferPtr = ProductOffer.objects.create(product_id=productOffer['productID'], offerType_id=productOffer['offerType'], description=productOffer['description'])
    except Exception as e:
        closeDBConnection()
        return customResponse("4XX", {"error": "unable to create entry in db"})

    closeDBConnection()
    return customResponse("2XX", {"productOffer": productOffers_parser([productOfferPtr])})

@csrf_exempt
def update_product_offer_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        productOffer = json.loads(request.body.decode("utf-8"))
        productOffer = convert_keys_to_string(productOffer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    if not len(productOffer):
        return customResponse("4XX", {"error": "Invaild data for product offer sent"})

    productOffer["description"] = json.dumps(convert_keys_to_string(productOffer["description"]))

    productOfferPtr = ProductOffer.objects.filter(id=productOffer["productOfferID"], product__distributor__id=distributorID)

    if not len(productOfferPtr):
        return customResponse("4XX", {"error": "No such offer exists"})

    productOfferPtr = productOfferPtr[0]
    try:
        productOfferPtr.description = convert_keys_to_string(productOffer["description"])
        productOfferPtr.save()
    except Exception as e:
        closeDBConnection()
        return customResponse("4XX", {"error": "unable to create entry in db"})

    closeDBConnection()
    return customResponse("2XX", {"productOffer": productOffers_parser([productOfferPtr])})

@csrf_exempt
def delete_product_offer_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        productOffer = json.loads(request.body.decode("utf-8"))
        productOffer = convert_keys_to_string(productOffer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    if not len(productOffer):
        return customResponse("4XX", {"error": "Invaild data for product offer sent"})

    productOffer["description"] = json.dumps(convert_keys_to_string(productOffer["description"]))

    productOfferPtr = ProductOffer.objects.filter(id=productOffer["productOfferID"], product__distributor__id=distributorID)

    if not len(productOfferPtr):
        return customResponse("4XX", {"error": "No such offer exists"})

    productOfferPtr = productOfferPtr[0]
    try:
        productOfferPtr.delete()
    except Exception as e:
        closeDBConnection()
        return customResponse("4XX", {"error": "unable to create entry in db"})

    closeDBConnection()
    return customResponse("2XX", {"productOffer": productOffers_parser([productOfferPtr])})
