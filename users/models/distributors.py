from django.db import models

from pincodes.models import Pincode

class Distributor(models.Model):

    name = models.CharField(max_length=120, blank=False)

    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    mobile_number = models.CharField(max_length=13, unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)

    company_name = models.CharField(max_length=60, blank=False, null=False)
    alternate_number = models.CharField(max_length=15, blank=True, null=False)
    company_logo = models.URLField(blank=True, null=False)
    year_established = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    company_website = models.URLField(blank=True, null=False)

    email_verification = models.BooleanField(default=0, blank=False, null=False)
    mobile_verification = models.BooleanField(default=0, blank=False, null=False)

    account_active = models.BooleanField(default=0, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    address_line_1 = models.CharField(max_length=200, blank=True, null=False)
    address_line_2 = models.CharField(max_length=200, blank=True, null=False)
    landmark = models.CharField(max_length=100, blank=True, null=False)
    latitude = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)

    pincode = models.ForeignKey(Pincode)

    pan = models.CharField(max_length=10, blank=True, null=False)
    name_on_pan = models.CharField(max_length=100, blank=True, null=False)
    dob_on_pan = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    pan_scanned_copy = models.FileField(upload_to=None, max_length=200, blank=True)

    tin = models.CharField(max_length=11, blank=True, null=False)
    tin_scanned_copy = models.FileField(upload_to=None, max_length=200, blank=True)

    pan_verification = models.BooleanField(default=0, blank=False, null=False)
    tin_verification = models.BooleanField(default=0, blank=False, null=False)

    def __str__(self):
        return self.company_name


class DistributorBankDetails(models.Model):

    distributor = models.ForeignKey(Distributor, models.CASCADE)

    account_holders_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=18)
    ifsc = models.CharField(max_length=11)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.distributor.company_name
