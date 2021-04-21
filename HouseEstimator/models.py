from django.utils import timezone
from django.db import models


class House(models.Model):
    area = models.IntegerField(null=False, blank=False)
    room_number = models.IntegerField(null=False, blank=False)
    year = models.IntegerField(null=False, blank=False)
    neighbourhood = models.TextField(max_length=400)
    price = models.IntegerField(default=-1)
    link = models.URLField(blank=True)
    slug = models.SlugField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.neighbourhood}, {self.area}, {self.room_number}, {self.year}"

    def get_abs_url(self):
        return f"/{self.slug}/"