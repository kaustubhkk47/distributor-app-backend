from django.contrib import admin

from .models.products import *
from .models.offers import *

admin.site.register(Offer)
admin.site.register(Product)
