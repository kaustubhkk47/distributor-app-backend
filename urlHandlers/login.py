from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings

from users.models.distributors import Distributor
from users.models.salesman import Salesman
from users.serializers.distributors import serialize_distributor
from scripts.utils import get_token_expiration
from scripts.utils import customResponse

import jwt as JsonWebToken


@csrf_exempt
def distributor_login(request):
    response = {}
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if not email or not password:
            return customResponse("4XX", {"error": "Either email or password was empty"})

        # if check_token(request)
        try:
            distributor = Distributor.objects.get(email=email)
        except Distributor.DoesNotExist:
            return customResponse("4XX", {"error": "Invalid distributor credentials"})

        if password == distributor.password:
            tokenPayload = {
                "user": "distributor",
                "distributorID": distributor.id,
            }

            encoded = JsonWebToken.encode(tokenPayload, settings.SECRET_KEY, algorithm='HS256')
            response = {
                "token": encoded.decode("utf-8"),
                "distributor": serialize_distributor(distributor)
            }
            return customResponse("2XX", response)
        else:
            return customResponse("4XX", {"error": "Invalid distributor credentials"})

    return customResponse("4XX", {"error": "Invalid request"})


@csrf_exempt
def salesman_login(request):
    response = {}
    if request.method == "POST":
        mobile_number = request.POST.get('mobile_number', '')
        password = request.POST.get('password', '')

        if not mobile_number or not password:
            return customResponse("4XX", {"error": "Either email or password was empty"})
        try:
            salesman = Salesman.objects.get(mobile_number=mobile_number)
        except Salesman.DoesNotExist:
            return customResponse("4XX", {"error": "Invalid salesman credentials"})

        tokenPayload = {
            "user": "salesman",
            "distributorID": salesman.distributor.id,
            "salesmanID": salesman.id
        }
        if password == salesman.password:
            encoded = JsonWebToken.encode(tokenPayload, settings.SECRET_KEY, algorithm='HS256')
            return customResponse("2XX", {"token": encoded.decode("utf-8")})
        else:
            return customResponse("4XX", {"error": "Invalid salesman credentials"})

    else:  ## request method block
        return customResponse("4XX",{"error":"Invalid request method"})
