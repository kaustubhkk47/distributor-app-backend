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
def add_new_offer(request, tokenPayload):
    distributorID = tokenPayload["distributorID"]

    try:
        offer = json.loads(request.body.decode("utf-8"))
        offer = convert_keys_to_string(offer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invliad data sent in request"})

    if not len(offer) or not 'title' in offer:
        return customResponse("4XX", {"error": "Invaild data for offer sent"})
    print offer
    try:
        newOffer = Offer.objects.create(distributor_id=distributorID, title=offer['title'])

    except Exception as e:
        closeDBConnection()
        return customResponse("4XX", {"error": "unable to create entry in db"})

    closeDBConnection()
    return customResponse("2XX", {"offers": offers_parser([newOffer])})

@csrf_exempt
def delete_offer(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        offer = json.loads(request.body.decode("utf-8"))
        offer = convert_keys_to_string(offer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invliad data sent in request"})

    if not 'offerID' in offer:
        return customResponse("4XX", {"error": "Invaild data for offer sent"})

    try:
        offerPtr = Offer.objects.get(id=int(offer["offerID"]))
    except Offer.DoesNotExist:
        closeDBConnection()
        return customResponse("4XX", {"error": "No such Offer exists"})

    if offerPtr.distributor_id != distributorID:
        return customResponse("4XX", {"error": "different distributor"})

    offerPtr.delete()
    closeDBConnection()
    return customResponse("2XX", {"offers": offers_parser([offerPtr])})

@csrf_exempt
def update_offer(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        offer = json.loads(request.body.decode("utf-8"))
        offer = convert_keys_to_string(offer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invliad data sent in request"})

    if not len(offer) or not 'title' in offer or not 'offerID' in offer:
        return customResponse("4XX", {"error": "Invaild data for offer sent"})

    offerPtr = Offer.objects.filter(id=offer["offerID"], distributor__id=distributorID)
    if len(offerPtr) == 0:
        closeDBConnection()
        return customResponse("4XX", {"error": "No such offer exists"})

    offerPtr = offerPtr[0]

    try:
        offerPtr.title = offer['title']
        offerPtr.save()
        closeDBConnection()
    except Exception as e:
        closeDBConnection()
        return customResponse("4XX", {"error": "could not update"})
    else:
        return customResponse("2XX", {"offer": offers_parser([offerPtr])})
