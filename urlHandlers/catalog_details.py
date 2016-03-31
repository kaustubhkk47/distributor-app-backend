from django.views.decorators.csrf import csrf_exempt

from catalog.views.offers import *
from catalog.views.products import *

from scripts.utils import customResponse, get_token_payload

def get_offers(request):
    tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")

    if not len(tokenPayload):
        return customResponse("4XX", {"error": "Invalid Token"})

    if request.method == "GET":
        return get_offer_details(request, tokenPayload)
    else:
        return customResponse("4XX", {"error": "invalid method"})

def get_products(request):
    tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")

    if not len(tokenPayload):
        return customResponse("4XX", {"error": "Invalid Token"})

    if request.method == "GET":
        return get_product_details(request, tokenPayload)
    else:
        return customResponse("4XX", {"error": "invalid method"})
