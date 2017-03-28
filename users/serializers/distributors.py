
def serialize_distributor(distributorItem):
    distributor = {
        "distributorID": distributorItem.id,
        "email": distributorItem.email,
        "mobile_number": distributorItem.mobile_number,
        "company_name": distributorItem.company_name,
        "name": distributorItem.name
    }
    return distributor

def distributor_parser():
    return {}
