from CarEstimator.models import Car
from csv import DictReader
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for row in DictReader(open('CarEstimator/Model/CarData.csv')):
            car = Car()
            car.pk = row['id']
            if row['price'] == 'nan':
                car.price = -1
            else:
                car.price = row['price']
            if row['year'] == 'nan':
                car.year = -1
            else:
                car.year = row['year']
            if row["link"] == 'nan':
                car.link = "https://bama.ir/"
            else:
                car.link = row['link']
            if row['mileage'] == 'nan' or row['mileage'] == '-':
                car.mileage = -1
            else:
                car.mileage = row['mileage']

            car.model = row['model']
            car.brand = row['brand']
            car.body_status = row['body_status']
            car.save()