from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings

from users.models.distributors import Distributor
from users.models.salesman import Salesman
from scripts.utils import get_token_expiration

import jwt as JsonWebToken


@csrf_exempt
def distributor_login(request):
    response = {}
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if not email or not password:
            response['statusCode'] = '4XX'
            response['error'] = 'Either email or password was empty'
            return JsonResponse(response)

        # if check_token(request)
        try:
            distributor = Distributor.objects.get(email=email)
        except Distributor.DoesNotExist:
            response['statusCode'] = '4XX'
            response['error'] = 'Invalid distributor credentials'
            return JsonResponse(response)

        if check_password(password,distributor.password):
            tokenPayload = {
                "user": "distributor",
                "distributorID": distributor.id,
                "exp": get_token_expiration()
            }

            encoded = JsonWebToken.encode(tokenPayload, settings.SECRET_KEY, algorithm='HS256')
            response['statusCode'] = '2XX'
            response['token'] = encoded.decode("utf-8")
            return JsonResponse(response)

        else:
            response['statusCode'] = '4XX'
            response['error'] = 'Invalid distributor credentials'
            return JsonResponse(response)

    response['statusCode'] = '4XX'
    response['error'] = 'invalid request'
    return JsonResponse(response)


@csrf_exempt
def salesman_login(request):
    response = {}
    if request.method == "POST":
        mobile_number = request.POST.get('mobile_number', '')
        password = request.POST.get('password', '')

        if not mobile_number or not password:
            response["statusCode"] = '4XX'
            response["error"] = 'Either email or password was empty'
        else:
            try:
                salesman = Salesman.objects.get(mobile_number=mobile_number)
            except Salesman.DoesNotExist:
                response["statusCode"] = "4XX"
                response["error"] = "Invalid salesman credentials"
                return JsonResponse(response)

            tokenPayload = {
                "user": "salesman",
                "distributorID": salesman.distributor.id,
                "salesmanID": salesman.id,
                "exp": get_token_expiration()
            }
            if check_password(password,salesman.password):
                encoded = JsonWebToken.encode(tokenPayload, settings.SECRET_KEY, algorithm='HS256')
                response["statusCode"] = '2XX'
                response["token"] = encoded.decode("utf-8")
                return JsonResponse(response)
            else:
                response["statusCode"] = "4XX"
                response["error"] = "Invalid salesman credentials"
                return JsonResponse(response)

            return JsonResponse(response)
    else:
        ## request method block
        response["statusCode"] = "4XX"
        response["error"] = "Invalid method"
        return JsonResponse(response)
