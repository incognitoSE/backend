from django.db import models


class Simcard(models.Model):
    CHOICES = ((0, 0), (1, 1))
    number = models.IntegerField(null=False, blank=False)
    rond = models.IntegerField(choices=CHOICES)
    stock = models.IntegerField(choices=CHOICES)
    daemi = models.IntegerField(choices=CHOICES)
    link = models.URLField(blank=True)
    price = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.number}"