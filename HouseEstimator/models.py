from django.utils import timezone
from django.db import models


class House(models.Model):
    link = models.URLField(blank=True)
    # wow = models.IntegerField()
    location = models.TextField(max_length=400, blank=False)
    area = models.IntegerField(null=False, blank=False)
    room = models.IntegerField(null=False, blank=False)
    year = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.location}, {self.area}, {self.room}, {self.year}"