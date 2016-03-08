from django.conf import settings
from django.http import JsonResponse

import jwt as JsonWebToken
import datetime


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
    return datetime.datetime.now() + datetime.timedelta(seconds=3600)


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
    if extension in ["jpeg", "png", "gif", "bmp"]:
        return True
    return False
