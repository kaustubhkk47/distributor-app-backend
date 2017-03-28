from django.views.decorators.csrf import csrf_exempt
import json

from scripts.utils import customResponse, convert_keys_to_string, closeDBConnection

from ..models.tracking import Tracking

def json_response(data):
    response = []
    for i in range(len(data)):
        tracking = {
            "id": data[i].id,
            "salesmanID": data[i].salesman_id,
            "latlngs": data[i].latlngs
        }
        response.append(tracking)
    return response

def get_tracking_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    salesmanID = request.GET.get("salesmanID", '')
    if salesmanID:
        tracking = Tracking.objects.filter(salesman__id=salesmanID)
    else:
        tracking = Tracking.objects.filter(salesman__distributor__id=distributorID)

    closeDBConnection()
    return customResponse("2XX", {"tracking": json_response(tracking)})

@csrf_exempt
def post_new_tracking_details(request, tokenPayload):
    salesmanID = tokenPayload['salesmanID']

    try:
        tracking = json.loads(request.body.decode("utf-8"))
        tracking = convert_keys_to_string(tracking)
        for i in range(len(tracking['latlngs'])):
            convert_keys_to_string(tracking['latlngs'][i])

    except Exception as e:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    if not len(tracking) or not 'latlngs' in tracking or not tracking['latlngs']:
        return customResponse("4XX", {"error": "Invaild data for tracking sent"})

    for i in range(len(tracking['latlngs'])):
        tracking['latlngs'][i] = convert_keys_to_string(tracking['latlngs'][i])

    try:
        newTracking = Tracking.objects.create(salesman_id=salesmanID, latlngs=json.dumps(tracking['latlngs']))
    except Exception as e:
        closeDBConnection()
        return customResponse("4XX", {"error": "unable to create entry in db"})

    closeDBConnection()
    return customResponse("2XX", {"tracking": json_response([newTracking])})
