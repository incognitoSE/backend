# Generated by Django 3.2 on 2021-05-02 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseEstimator', '0004_alter_house_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='year',
            field=models.CharField(max_length=10),
        ),
    ]
