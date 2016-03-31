
from ..models.offers import Offer

from ..serializers.offers import offers_parser

from scripts.utils import customResponse

def get_offer_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    offers = Offer.objects.filter(distributor__id=distributorID)

    print offers
    return customResponse("2XX", {"offers": offers_parser(offers)})
