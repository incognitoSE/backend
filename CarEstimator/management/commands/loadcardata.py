from CarEstimator.models import Car
from csv import DictReader
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for row in DictReader(open('CarEstimator/Model/CarData.csv')):
            car = Car()
            car.pk = row['id']
            car.price = -1 if row['price'] == 'nan' else row['price']
            car.year = -1 if row['year'] == 'nan' else row['year']
            car.link = "https://bama.ir/" if row["link"] == 'nan' else row['link']
            car.mileage = -1 if row['mileage'] in ['nan', '-'] else row['mileage']
            car.model = row['model']
            car.brand = row['brand']
            car.body_status = row['body_status']
            car.save()