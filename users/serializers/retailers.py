import time

def serialize_retailer(retailerItem):
    retialer = {
        "retailerID": retailerItem.id,
        "company_name": retailerItem.company_name,
        "name": retailerItem.get_full_name(),
        "mobile_number": retailerItem.mobile_number,
        "profile_picture": retailerItem.profile_picture.url if retailerItem.profile_picture else "",
        "address": retailerItem.get_address(),
        "latitude": retailerItem.latitude,
        "longitude": retailerItem.longitude,
        "created_at": time.mktime(retailerItem.created_at.timetuple()),
        "updated_at": time.mktime(retailerItem.updated_at.timetuple())
    }
    return retialer

def retailer_parser(retialerQuerySet):
    retailers = []

    for i in range(len(retialerQuerySet)):
        retailers.append(serialize_retailer(retialerQuerySet[i]))

    return retailers
