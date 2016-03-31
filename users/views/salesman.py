from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import make_password

from ..models.salesman import Salesman

from ..models.distributors import Distributor

from ..serializers.salesman import salesman_parser

from scripts.utils import customResponse,check_mobile_number,check_valid_image

def get_salesman_details(tokenPayload, salesmanID=0):
    distributorID = tokenPayload["distributorID"]

    try:
        salesmanID = int(salesmanID)
        if salesmanID > 0:
            salesmen = Salesman.objects.get(distributor__id=distributorID, id=salesmanID, account_active=True)
            salesmen = [salesmen]
        else:
            salesmen = Salesman.objects.filter(distributor__id=distributorID, account_active=True)
    except Exception as e:
        return customResponse("4XX", {"error": "No Salesman Found"})

    return customResponse("2XX", {"salesmen": salesman_parser(salesmen)})


@csrf_exempt
def post_new_salesman(request, tokenPayload):
    distributorID = tokenPayload["distributorID"]

    try:
        # no need to validate,will automatically raise an exception if not found
        assocDistributor = Distributor.objects.get(id=distributorID)
        # validating length of mobile number
        mobileNumber = request.POST.get('mobile_number')
        if not check_mobile_number(mobileNumber):
            return customResponse("4XX", {"error": "Invalid mobile number"})

        # no need to validate, will raise a exception if empty
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name', '')
        password = make_password(request.POST.get('password'))

        profilePicture = request.FILES.get('profile_picture', '')
        if not profilePicture == '' and not check_valid_image(profilePicture.name):
            return customResponse("4XX",{"error":"Invalid image format"})

        salesman, created = Salesman.objects.get_or_create(mobile_number=mobileNumber,
                                                           defaults={'first_name': firstName, 'last_name': lastName,
                                                                     'password': password,
                                                                     'profile_picture': profilePicture,
                                                                     'distributor': assocDistributor})

        if created == False:
            if salesman.distributor.id == distributorID:
                return customResponse("4XX", {"error": "Salesman  already exist"})
            elif salesman.account_active == 1:
                return customResponse("4XX",
                                      {"error": "Salesman already exists and is associated with another distributor"})
            else:
                salesman.distributor = assocDistributor
                salesman.account_active = 1
                salesman.save()
        salesman=[salesman]
        return customResponse("2XX", {"salesman": salesman_parser(salesman)})
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid request"})
