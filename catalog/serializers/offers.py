import time, json

def serialize_offer(offerItem):
    offer = {
        "offerID": offerItem.id,
        "distributorID": offerItem.distributor_id,
        "title": offerItem.title,
        "offer_status": offerItem.offer_status,
        "created_at": time.mktime(offerItem.created_at.timetuple())*1000,
        "updated_at": time.mktime(offerItem.updated_at.timetuple())*1000
    }
    return offer


def offers_parser(offerQuerySet):
    offers = []

    for i in range(len(offerQuerySet)):
        offers.append(serialize_offer(offerQuerySet[i]))

    return offers

def serialize_orderOffer(orderOfferItem):
    orderOffer = {
        "distributorID": orderOfferItem.distributor_id,
        "discount": orderOfferItem.discount,
        "name": orderOfferItem.name,
        "created_at": time.mktime(orderOfferItem.created_at.timetuple())*1000,
        "updated_at": time.mktime(orderOfferItem.updated_at.timetuple())*1000
    }
    return orderOffer

def orderOffers_parser(orderOffersQuerySet):
    orderOffers = []

    for i in range(len(orderOffersQuerySet)):
        orderOffers.append(serialize_orderOffer(orderOffersQuerySet[i]))
    return orderOffers


def serialize_productOffer(productOfferItem):
    productOffer = {
        "productID": productOfferItem.product_id,
        "offerType": {
            "offerTypeID": productOfferItem.offerType.id,
            "offerTypeName": productOfferItem.offerType.name
        },
        "description": json.loads(productOfferItem.description),
        "created_at": time.mktime(productOfferItem.created_at.timetuple())*1000,
        "updated_at": time.mktime(productOfferItem.updated_at.timetuple())*1000
    }
    return productOffer

def productOffers_parser(productOffersQuerySet):
    productOffers = []

    for i in range(len(productOffersQuerySet)):
        productOffers.append(serialize_productOffer(productOffersQuerySet[i]))
    return productOffers
