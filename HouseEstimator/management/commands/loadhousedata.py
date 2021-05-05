from HouseEstimator.models import House
from csv import DictReader
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for row in DictReader(open('HouseEstimator/Model/house_database.csv')):
            house = House()
            house.pk = row['id']
            house.area = row['area']
            house.price = row['price']
            house.room = row['room']
            if row["year"]:
                house.year = int(float(row['year']))
            else:
                house.year = -1
            house.location = row['location']
            house.link = row['link']
            house.save()