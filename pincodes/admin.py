from django.contrib import admin

from .models.city import City
from .models.country import Country
from .models.pincode import Pincode
from .models.state import State

admin.site.register(City)
admin.site.register(Country)
admin.site.register(Pincode)
admin.site.register(State)
