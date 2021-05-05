from django.utils import timezone
from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=100, null=False, blank=False)
    model = models.CharField(max_length=100, null=False, blank=False)
    mileage = models.IntegerField(null=False, blank=False)
    year = models.IntegerField(null=False, blank=False)
    body_status = models.CharField(max_length=100, null=False, blank=False)
    price = models.IntegerField(default=-1)
    link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.brand}, {self.model}, {self.year}, {self.mileage}"
