# Generated by Django 3.2 on 2021-04-14 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseEstimator', '0010_alter_house_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='price',
            field=models.IntegerField(default=-1),
        ),
    ]
