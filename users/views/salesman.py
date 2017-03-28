from django.views.decorators.csrf import csrf_exempt

from ..models.salesman import Salesman

from ..models.distributors import Distributor

from ..serializers.salesman import salesman_parser

from scripts.utils import customResponse, check_mobile_number, check_valid_image, convert_keys_to_string, closeDBConnection

import json

def get_salesman_details(tokenPayload, salesmanID=0):
    distributorID = tokenPayload["distributorID"]

    try:
        salesmanID = int(salesmanID)
        if salesmanID > 0:
            salesmen = Salesman.objects.get(distributor__id=distributorID, id=salesmanID, account_active=True)
            salesmen = [salesmen]
        else:
            salesmen = Salesman.objects.filter(distributor__id=distributorID, account_active=True)
            closeDBConnection()
    except Exception as e:
        return customResponse("4XX", {"error": "No Salesman Found"})

    return customResponse("2XX", {"salesmen": salesman_parser(salesmen)})


@csrf_exempt
def post_new_salesman(request, tokenPayload):
    distributorID = tokenPayload["distributorID"]

    try:
        salesman = json.loads(request.body.decode("utf-8"))
        salesman = convert_keys_to_string(salesman)
    except Exception as e:
        print e
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    if not len(salesman) or not 'mobile_number' in salesman or not salesman['mobile_number'] or not 'password' in salesman or not salesman['password']:
        return customResponse("4XX", {"error": "Invaild data for salesman sent"})

    if Salesman.objects.filter(distributor__id=distributorID, mobile_number=salesman['mobile_number']).exists():
        return customResponse("4XX", {"error": "Salesman already exist"})

    try:
        newSalesman = Salesman.objects.create(distributor_id=distributorID, mobile_number=salesman['mobile_number'], name=salesman['name'], password=salesman['password'])
    except Exception as e:
        print e
        closeDBConnection()
        return customResponse("4XX", {"error": "unable to create entry in db"})

    return customResponse("2XX", {"salesmen": salesman_parser([newSalesman])})


@csrf_exempt
def update_salesman(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        salesman = json.loads(request.body.decode("utf-8"))
        retailer = convert_keys_to_string(salesman)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    print salesman
    if not len(salesman) or not 'mobile_number' in salesman or not salesman['mobile_number'] or not 'password' in salesman or not salesman['password']:
        return customResponse("4XX", {"error": "Invaild data for salesman sent"})

    salesmanPtr = Salesman.objects.filter(id=int(salesman["salesmanID"]), distributor__id=distributorID)
    salesmanPtr = salesmanPtr[0]

    try:

        salesmanPtr.mobile_number = salesman['mobile_number']
        salesmanPtr.name = salesman['name']
        salesmanPtr.password = salesman['password']

        salesmanPtr.save()

        print salesmanPtr

    except Exception as e:
        print e
        closeDBConnection()
        return customResponse("4XX", {"error": "could not update"})
    else:
        closeDBConnection()
        return customResponse("2XX", {"retailer": salesman_parser([salesmanPtr])})

@csrf_exempt
def delete_salesman(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    try:
        salesman = json.loads(request.body.decode("utf-8"))
        salesman = convert_keys_to_string(salesman)
    except Exception as e:
        return customResponse("4XX", {"error": "Invalid data sent in request"})

    print salesman
    if not 'salesmanID' in salesman:
        return customResponse("4XX", {"error": "Invaild data for salesman sent"})

    try:
        salesmanPtr = Salesman.objects.get(id=int(salesman["salesmanID"]))
    except Salesman.DoesNotExist:
        closeDBConnection()
        return customResponse("4XX", {"error": "No such retailer exists"})

    if salesmanPtr.distributor_id != distributorID:
        return customResponse("4XX", {"error": "different distributor"})

    salesmanPtr.delete()
    closeDBConnection()
    return customResponse("2XX", {"retailer": salesman_parser([salesmanPtr])})
