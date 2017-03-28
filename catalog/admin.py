from django.contrib import admin

from .models.products import *
from .models.offers import *

admin.site.register(OfferType)
admin.site.register(Offer)
admin.site.register(OrderOffer)
admin.site.register(ProductOffer)
admin.site.register(Product)
