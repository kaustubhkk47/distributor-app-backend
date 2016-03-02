from django.views.decorators.csrf import csrf_exempt

from ..models.retailers import Retailer

from ..serializers.retailers import retailer_parser

from scripts.utils import customResponse

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
        return customResponse("4XX", "Invalid Retailer")

    return customResponse("2XX", {"retailers":retailer_parser(retailers)})

@csrf_exempt
def post_new_retailer(request, tokenPayload):
    return customResponse("4XX", "unbale to save")
