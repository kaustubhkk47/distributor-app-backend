from django.db import models

from .distributors import Distributor
from pincodes.models import Pincode

class Retailer(models.Model):

    distributors = models.ForeignKey(Distributor,models.SET_NULL,blank=True,null=True)

    company_name = models.CharField(max_length=100, blank=False)

    ## contact info for retailer can be added if required
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)

    mobile_number = models.CharField(max_length=13, blank=False, null=False)

    profile_picture = models.ImageField(upload_to=None, max_length=200, blank=True, null=False)

    address_line_1 = models.CharField(max_length=200, blank=True, null=False)
    address_line_2 = models.CharField(max_length=200, blank=True, null=False)
    landmark = models.CharField(max_length=100, blank=True, null=False)
    latitude = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)

    pincode = models.ForeignKey(Pincode)

    account_active = models.BooleanField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_address(self):
        address = self.address_line_1
        if self.address_line_2:
            address += ", " + self.address_line_2
        if self.landmark:
            address += ", " + self.landmark
        if self.pincode:
            address += ", " + self.pincode.city.name + ", " + self.pincode.city.state.name + ", " + self.pincode.pincode
        return address
