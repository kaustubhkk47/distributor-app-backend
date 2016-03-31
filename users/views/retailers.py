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
    if not "mobileNumber" in retailer or not check_mobile_number(retailer["mobileNumber"]):
        return False
    if not 'companyName' in retailer or not 'firstName' in retailer or not 'addressLine1' in retailer:
        return False
    if not 'pincode' in retailer or not check_pin_code_validity(retailer['pincode']):
        return False
    if not 'latitude' in retailer or not float(retailer['latitude']):
        retailer['latitude'] = 0.00
    if not 'longitude' in retailer or not float(retailer['longitude']):
        retailer['longitude'] = 0.00
    if not 'landmark' in retailer:
        retailer['landmark'] = ""
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

    if Retailer.objects.filter(distributors__id=distributorID, mobile_number=str(retailer['mobileNumber'])).exists():
        return customResponse("4XX", {"error": "Retailer already exist"})

    try:
        pincode = Pincode.objects.get(pincode=retailer['pincode'])
        newRetailer = Retailer.objects.create(mobile_number=retailer['mobileNumber'], company_name=retailer['companyName'], first_name=retailer['firstName'],
                                              last_name=retailer['lastName'], address_line_1=retailer['addressLine1'],
                                              address_line_2=retailer['addressLine2'], landmark=retailer['landmark'],
                                              latitude=retailer['latitude'], longitude=retailer['longitude'],
                                              pincode=pincode, distributors_id=distributorID)
    except Exception as e:
        return customResponse("4XX", {"error": "unable to create entry in db"})
    else:
        return customResponse("2XX", {"retailer": retailer_parser([newRetailer])})
