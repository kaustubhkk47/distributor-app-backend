from django.views.decorators.csrf import csrf_exempt

from ..models.salesman import Salesman

from ..models.distributors import Distributor

from ..serializers.salesman import salesman_parser

from scripts.utils import customResponse


def get_salesman_details(tokenPayload, salesmanID=0):
    distributorID = tokenPayload["distributorID"]

    try:
        salesmanID = int(salesmanID)
        if salesmanID > 0:
            salesmen = Salesman.objects.get(distributor__id=distributorID, id=salesmanID,account_active=True)
            salesmen = [salesmen]
        else:
            salesmen = Salesman.objects.filter(distributor__id=distributorID,account_active=True)
    except Exception as e:
        return customResponse("4XX", "No Salesman Found")

    return customResponse("2XX", {"salesmen": salesman_parser(salesmen)})


@csrf_exempt
def post_new_salesman(request, tokenPayload):
    distributorID = tokenPayload["distributorID"]

    try:
        assocDistributor = Distributor.objects.get(id=distributorID)
        mobileNumber = request.POST.get('mobile_number')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name', '')
        password = request.POST.get('password')
        profilePicture = request.POST.get('profile_picture', '')
        salesman, created = Salesman.objects.get_or_create(mobile_number=mobileNumber,
                                                           defaults={'first_name': firstName, 'last_name': lastName,
                                                                     'password': password,
                                                                     'profile_picture': profilePicture,
                                                                     'distributor': assocDistributor})

        if created == False:
            if salesman.distributor.id == distributorID:
                return customResponse("4XX", "Salesman  already exist")
            elif salesman.account_active == 1:
                return customResponse("4XX", "Salesman already exists and is associated with another distributor")
            else:
                salesman.distributor = assocDistributor
                salesman.account_active = 1
                salesman.save()
        return customResponse("2XX", "Salesman created")
    except Exception as e:
        return customResponse("4XX", "Invalid request")
