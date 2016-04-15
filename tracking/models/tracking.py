from django.db import models

from users.models.salesman import Salesman

class Tracking(models.Model):
    salesman = models.ForeignKey(Salesman)
    latlngs = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.salesman.name
