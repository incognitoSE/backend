# Generated by Django 3.2 on 2021-05-02 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CarEstimator', '0003_alter_car_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='car',
            name='slug',
        ),
    ]