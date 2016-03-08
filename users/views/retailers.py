from django.views.decorators.csrf import csrf_exempt

from ..models.retailers import Retailer

from ..models.distributors import Distributor

from pincodes.models import Pincode

from ..serializers.retailers import retailer_parser

from scripts.utils import customResponse, check_mobile_number, check_valid_image


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

    try:
        mobileNumber = request.POST.get('mobile_number')
        if not check_mobile_number(mobileNumber):
            return customResponse("4XX", {"error": "Invalid mobile number"})

        if Retailer.objects.filter(distributors__id=distributorID, mobile_number=mobileNumber).exists():
            return customResponse("4XX", "Retailer already exist")

        companyName = request.POST.get('company_name')
        firstName = request.POST.get('first_name', '')
        lastName = request.POST.get('last_name', '')

        profilePicture = request.FILES.get('profile_picture', '')
        if not profilePicture == '' and not check_valid_image(profilePicture.name):
            return customResponse("4XX", {"error": "Invalid image format"})

        addressLine1 = request.POST.get('address_line1', '')
        addressLine2 = request.POST.get('address_line2', '')
        retLandmark = request.POST.get('landmark', '')

        retLatitude = request.POST.get('latitude', 0)
        if not retLatitude.isdecimal():
            return customResponse("4XX", {"error": "Invalid latitude"})
        retLongitude = request.POST.get('longitude', 0)
        if not retLatitude.isdecimal():
            return customResponse("4XX", {"error": "Invalid latitude"})

        retPincode = request.POST.get('pincode')
        pincode = Pincode.objects.get(pincode=retPincode)
        assocDistributor = Distributor.objects.get(id=distributorID)

        retailer = Retailer.objects.create(company_name=companyName, first_name=firstName, last_name=lastName,
                                           mobile_number=mobileNumber,
                                           profile_picture=profilePicture, address_line_1=addressLine1,
                                           address_line_2=addressLine2, landmark=retLandmark, latitude=retLatitude,
                                           longitude=retLongitude, pincode=pincode, distributors=assocDistributor)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid request"})
    return customResponse("2XX", {"retailer": retailer_parser(retailer)})
