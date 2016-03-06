from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from users.views import *
from users.models.distributors import Distributor
from users.models.salesman import Salesman


from users.serializers.distributors import distributor_parser
from users.serializers.salesman import salesman_parser


from scripts.utils import customResponse, get_token_payload

@csrf_exempt
def retailer_details(request, retailerID=0):
    tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")

    if not len(tokenPayload):
        return customResponse("4XX", {"error": "Invalid Token"})

    if request.method == "GET":
        return retailers.get_retailer_details(tokenPayload, retailerID)
    elif request.method == "POST":
        return retailers.post_new_retailer(request, tokenPayload)

    return customResponse("4XX", {"error": "Invalid request"})

def distributor_details(distributorID):
    return customResponse("4XX", {"error": "Invalid request"})

@csrf_exempt
def salesman_details(request,salesmanID=0):
    tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")

    if not len(tokenPayload):
        return customResponse("4xx", {"error": "Invalid Token"})

    if request.method == "GET":
        return salesman.get_salesman_details(tokenPayload, salesmanID)
    elif request.method == "POST":
        return salesman.post_new_salesman(request, tokenPayload)
   
    return customResponse("4XX", {"error": "Invalid request"})
