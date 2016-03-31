from django.db import models

from .distributors import Distributor


class Salesman(models.Model):
    distributor = models.ForeignKey(Distributor, models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=120, blank=False)

    mobile_number = models.CharField(max_length=13, unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)

    profile_picture = models.ImageField(upload_to=None, max_length=200, blank=True, null=False)

    account_active = models.BooleanField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
