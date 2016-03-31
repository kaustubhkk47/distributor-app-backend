from ..models.products import Product

from ..serializers.products import products_parser

from scripts.utils import customResponse

def get_product_details(request, tokenPayload):
    distributorID = tokenPayload['distributorID']

    products = Product.objects.filter(distributor__id=distributorID)

    return customResponse("2XX", {"products": products_parser(products)})
