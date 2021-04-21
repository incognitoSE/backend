# Generated by Django 3.2 on 2021-04-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.IntegerField()),
                ('room_number', models.IntegerField()),
                ('year', models.IntegerField()),
                ('link', models.URLField()),
            ],
        ),
    ]
