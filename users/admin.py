from django.contrib import admin

from .models.distributors import *
from .models.retailers import *
from .models.salesman import *

admin.site.register(Distributor)
admin.site.register(DistributorBankDetails)
admin.site.register(Salesman)
admin.site.register(Retailer)
