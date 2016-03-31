import time
from scripts.utils import get_image_url


def serialize_salesman(salesmanData):
    salesman = {
        "salesmanID": salesmanData.id,
        "name": salesmanData.name,
        "mobile_number": salesmanData.mobile_number,
        "profile_picture": get_image_url(salesmanData.profile_picture),
        "created_at": time.mktime(salesmanData.created_at.timetuple()),
        "updated_at": time.mktime(salesmanData.updated_at.timetuple())

    }
    return salesman


def salesman_parser(salesmanQuerySet):
    salesmen = []

    for i in range(len(salesmanQuerySet)):
        salesmen.append(serialize_salesman(salesmanQuerySet[i]))

    return salesmen
