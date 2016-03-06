import time


def serialize_salesman(salesmanData):
    salesman = {
        "salesmanID": salesmanData.id,
        "name": salesmanData.get_full_name(),
        "mobile_number": salesmanData.mobile_number,
        "profile_picture": salesmanData.profile_picture.url if salesmanData.profile_picture else "",
        "created_at": time.mktime(salesmanData.created_at.timetuple()),
        "updated_at": time.mktime(salesmanData.updated_at.timetuple())

    }
    return salesman


def salesman_parser(salesmanQuerySet):
    salesmen = []

    for i in range(len(salesmanQuerySet)):
        salesmen.append(serialize_salesman(salesmanQuerySet[i]))

    return salesmen
