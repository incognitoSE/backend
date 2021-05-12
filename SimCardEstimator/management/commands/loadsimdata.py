from SimCardEstimator.models import Simcard
from csv import DictReader
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for row in DictReader(open('SimCardEstimator/Model/SimData.csv')):
            sim = Simcard()
            sim.pk = row['id']
            sim.number = row['number']
            sim.rond = row['rond']
            sim.stock = row['stock']
            sim.daemi = row['daemi']
            sim.link = row['link']
            sim.price = row['price']
            sim.save()