from django.views.decorators.csrf import csrf_exempt

from tracking.views import *

from scripts.utils import customResponse, get_token_payload

@csrf_exempt
def tracking_details(request):
    if request.method == "GET":
        tokenPayload = get_token_payload(request.GET.get("access_token", ""), "distributorID")
        if not len(tokenPayload):
            return customResponse("4XX", {"error": "Invalid Token"})
        return tracking.get_tracking_details(request, tokenPayload)

    elif request.method == "POST":
        tokenPayload = get_token_payload(request.GET.get("access_token", ""), "salesmanID")
        if not len(tokenPayload):
            return customResponse("4XX", {"error": "Invalid Token"})
        return tracking.post_new_tracking_details(request, tokenPayload)
    # elif request.method == "PUT":
    #     return retailers.update_retailer(request, tokenPayload)
    # elif request.method == "DELETE":
    #     return retailers.delete_retailer(request, tokenPayload)

    return
