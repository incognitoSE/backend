# Generated by Django 3.1.7 on 2021-05-04 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseEstimator', '0005_alter_house_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='house',
            name='year',
            field=models.IntegerField(),
        ),
    ]