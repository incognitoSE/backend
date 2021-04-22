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
    slug = models.SlugField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.brand}, {self.model}, {self.year}, {self.mileage}"

    def get_abs_url(self):
        return f"/{self.slug}/"
