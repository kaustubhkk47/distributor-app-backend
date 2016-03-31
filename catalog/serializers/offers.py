import time

def serialize_retailer(offerItem):
    offer = {
        "offerID": offerItem.id,
        "distributorID": offerItem.distributor_id,
        "title": offerItem.title,
        "offer_status": offerItem.offer_status,
        "created_at": time.mktime(offerItem.created_at.timetuple()),
        "updated_at": time.mktime(offerItem.updated_at.timetuple())
    }
    return offer


def offers_parser(offerQuerySet):
    offers = []

    for i in range(len(offerQuerySet)):
        offers.append(serialize_retailer(offerQuerySet[i]))

    return offers
