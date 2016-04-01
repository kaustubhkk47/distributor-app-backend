from django.views.decorators.csrf import csrf_exempt

from orders.views import *

from scripts.utils import customResponse, get_token_payload

def get_orders(request):
    tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")

    if not len(tokenPayload):
        return customResponse("4XX", {"error": "Invalid Token"})

    if request.method == "GET":
        return orders.get_orders_details(request, tokenPayload)
    else:
        return customResponse("4XX", {"error": "Invalid method"})
