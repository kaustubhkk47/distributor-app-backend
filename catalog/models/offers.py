from django.db import models

from users.models.distributors import Distributor

class Offer(models.Model):

    distributor = models.ForeignKey(Distributor, models.SET_NULL, blank=True, null=True)

    title = models.CharField(max_length=200, blank=False, null=False)
    offer_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
