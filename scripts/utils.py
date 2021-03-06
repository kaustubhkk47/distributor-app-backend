from django.conf import settings
from django.http import JsonResponse
from django.db import connection

import jwt as JsonWebToken
import datetime

def closeDBConnection():
    connection.close()

def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v))
        for k, v in dictionary.items())

def check_token_validity(access_token):
    if not access_token:
        ## log the exception into db
        return {}
    try:
        tokenPayload = JsonWebToken.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    except Exception as ex:
        ## log the exception into db
        return {}

    return tokenPayload


def get_token_payload(access_token, userID):
    tokenPayload = check_token_validity(access_token)

    if not "user" in tokenPayload or not userID in tokenPayload:
        return {}

    return tokenPayload


def get_token_expiration():
    return datetime.datetime.now() + datetime.timedelta(seconds=36000)


def customResponse(statusCode, body):
    response = {}
    response["statusCode"] = statusCode
    response["body"] = body

    return JsonResponse(response)


def get_image_url(image):
    if not image:
        return ""
    return image.url


def check_mobile_number(number):
    if number.isnumeric() and len(number) == 10:
        return True
    return False


def check_valid_image(image):
    if image == '':
        return True
    description = image.split('.')
    extension = str(description[-1]).lower()
    if extension in ["jpg", "jpeg", "png", "gif", "bmp"]:
        return True
    return False

def check_pin_code_validity(pincode):
    if not pincode:
        return False
    elif len(str(pincode)) != 6:
        return False
    return True