from django.views.decorators.csrf import csrf_exempt

from ..models.retailers import Retailer

from ..models.distributors import Distributor

from pincodes.models import Pincode

from ..serializers.retailers import retailer_parser

from scripts.utils import customResponse, check_mobile_number, check_valid_image, check_pin_code_validity

import json

def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v))
        for k, v in dictionary.items())

def validateRetailerData(retailer):
    print "validate"
    print retailer
    if not "mobile_number" in retailer or not check_mobile_number(retailer["mobile_number"]):
        return False
    if not 'company_name' in retailer or not 'name' in retailer or not 'address_line_1' in retailer:
        return False
    if not 'pincode' in retailer or not check_pin_code_validity(retailer['pincode']):
        return False
    if not 'latitude' in retailer or not retailer['latitude']:
        retailer['latitude'] = None
    if not 'longitude' in retailer or not retailer['longitude']:
        retailer['longitude'] = None
    if not 'landmark' in retailer:
        retailer['landmark'] = None
    return True

def get_retailer_details(tokenPayload, retailerID=0):
    distributorID = tokenPayload["distributorID"]

    try:
        retailerID = int(retailerID)
        if retailerID > 0:
            retailers = Retailer.objects.get(distributors__id=distributorID, id=retailerID, account_active=True)
            retailers = [retailers]
        else:
            retailers = Retailer.objects.filter(distributors__id=distributorID, account_active=True)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid Retailer"})

    return customResponse("2XX", {"retailers": retailer_parser(retailers)})


@csrf_exempt
def post_new_retailer(request, tokenPayload):
    distributorID = tokenPayload["distributorID"]

    ## get information from request.body
    try:
        retailer = json.loads(request.body.decode("utf-8"))
        retailer = convert_keys_to_string(retailer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invliad data sent in request"})

    if not len(retailer) or not validateRetailerData(retailer):
        return customResponse("4XX", {"error": "Invaild data for retailer sent"})

    if Retailer.objects.filter(distributors__id=distributorID, mobile_number=str(retailer['mobile_number'])).exists():
        return customResponse("4XX", {"error": "Retailer already exist"})

    try:
        pincode = Pincode.objects.get(pincode=retailer['pincode'])
        newRetailer = Retailer.objects.create(mobile_number=retailer['mobile_number'], company_name=retailer['company_name'], name=retailer['name'],
                                              address_line_1=retailer['address_line_1'],
                                              address_line_2=retailer['address_line_2'], landmark=retailer['landmark'],
                                              latitude=retailer['latitude'], longitude=retailer['longitude'],
                                              pincode=pincode, distributors_id=distributorID)
    except Exception as e:
        return customResponse("4XX", {"error": "unable to create entry in db"})
    else:
        return customResponse("2XX", {"retailer": retailer_parser([newRetailer])})

@csrf_exempt
def update_retailer(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        retailer = json.loads(request.body.decode("utf-8"))
        retailer = convert_keys_to_string(retailer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invliad data sent in request"})

    print retailer
    if not len(retailer) or not validateRetailerData(retailer):
        return customResponse("4XX", {"error": "Invaild data for retailer sent"})

    retailerPtr = Retailer.objects.filter(id=int(retailer["retailerID"]), distributors__id=distributorID)
    retailerPtr = retailerPtr[0]

    if not retailer['latitude'] and retailerPtr.latitude:
        retailer['latitude'] = retailerPtr.latitude
    if not retailer['longitude'] and retailerPtr.longitude:
        retailer['longitude'] = retailerPtr.longitude

    try:
        pincode = Pincode.objects.get(pincode=retailer['pincode'])

        retailerPtr.mobile_number = retailer['mobile_number']
        retailerPtr.company_name = retailer['company_name']
        retailerPtr.name = retailer['name']
        retailerPtr.address_line_1 = retailer['address_line_1']
        retailerPtr.address_line_2 = retailer['address_line_2']
        retailerPtr.landmark = retailer['landmark']
        retailerPtr.pincode = pincode
        retailerPtr.latitude = retailer['latitude']
        retailerPtr.longitude = retailer['longitude']

        retailerPtr.save()

        print retailerPtr
        return customResponse("2XX", {"retailer": retailer_parser([retailerPtr])})

    except Exception as e:
        print e
        return customResponse("4XX", {"error": "could not update"})

@csrf_exempt
def delete_retailer(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        retailer = json.loads(request.body.decode("utf-8"))
        retailer = convert_keys_to_string(retailer)
    except Exception as e:
        return customResponse("4XX", {"error": "Invliad data sent in request"})

    print retailer
    if not 'retailerID' in retailer:
        return customResponse("4XX", {"error": "Invaild data for retailer sent"})

    try:
        retailerPtr = Retailer.objects.get(id=int(retailer["retailerID"]))
    except Retailer.DoesNotExist:
        return customResponse("4XX", {"error": "No such retailer exists"})

    if retailerPtr.distributors_id != distributorID:
        return customResponse("4XX", {"error": "different distributors"})

    retailerPtr.delete()

    return customResponse("2XX", {"retailer": retailer_parser([retailerPtr])})
