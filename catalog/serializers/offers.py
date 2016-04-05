import time

def serialize_offer(offerItem):
    offer = {
        "offerID": offerItem.id,
        "distributorID": offerItem.distributor_id,
        "title": offerItem.title,
        "offer_status": offerItem.offer_status,
        #"created_at": time.mktime(offerItem.created_at.timetuple()),
        "created_at": offerItem.created_at,
        "updated_at": time.mktime(offerItem.updated_at.timetuple())*1000
        #"updated_at": offerItem.updated_at
    }
    return offer


def offers_parser(offerQuerySet):
    offers = []

    for i in range(len(offerQuerySet)):
        offers.append(serialize_offer(offerQuerySet[i]))

    return offers
