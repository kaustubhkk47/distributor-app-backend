from django.views.decorators.csrf import csrf_exempt

from catalog.views.offers import *
from catalog.views.products import *

from scripts.utils import customResponse, get_token_payload

@csrf_exempt
def get_offers(request):
    tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")

    if not len(tokenPayload):
        return customResponse("4XX", {"error": "Invalid Token"})

    if request.method == "GET":
        return get_offer_details(request, tokenPayload)
    # elif request.method == "POST":
    #     return add_new_offer(request, tokenPayload)
    # elif request.method == "DELETE":
    #     return delete_offer(request, tokenPayload)
    # elif request.method == "PUT":
    #     return update_offer(request, tokenPayload)
    else:
        return customResponse("4XX", {"error": "invalid method"})

@csrf_exempt
def get_products(request):
    tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")

    if not len(tokenPayload):
        return customResponse("4XX", {"error": "Invalid Token"})

    if request.method == "GET":
        return get_product_details(request, tokenPayload)
    elif request.method == "POST":
        return post_new_product(request, tokenPayload)
    elif request.method == "PUT":
        return update_product_details(request, tokenPayload)
    elif request.method == "DELETE":
        return delete_product(request, tokenPayload)
    else:
        return customResponse("4XX", {"error": "invalid method"})

def get_offer_types(request):
    tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")

    if not len(tokenPayload):
        return customResponse("4XX", {"error": "Invalid Token"})

    if request.method == "GET":
        return get_offer_types_details(request, tokenPayload)
    else:
        return customResponse("4XX", {"error": "invalid method"})

@csrf_exempt
def product_offer_details(request):
    tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")

    if not len(tokenPayload):
        return customResponse("4XX", {"error": "Invalid Token"})

    # if request.method == "GET":
    #     return get_product_offer_details(request, tokenPayload)
    if request.method == "POST":
        return post_new_product_offer_details(request, tokenPayload)
    elif request.method == "PUT":
        return update_product_offer_details(request, tokenPayload)
    elif request.method == "DELETE":
        return delete_product_offer_details(request, tokenPayload)
    else:
        return customResponse("4XX", {"error": "invalid method"})

@csrf_exempt
def order_offer_details(request):
    tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")

    if not len(tokenPayload):
        return customResponse("4XX", {"error": "Invalid Token"})
        
    if request.method == "POST":
        return post_new_order_offer_details(request, tokenPayload)
    elif request.method == "PUT":
        return update_order_offer_details(request, tokenPayload)
    elif request.method == "DELETE":
        return delete_order_offer_details(request, tokenPayload)
    else:
        return customResponse("4XX", {"error": "invalid method"})
