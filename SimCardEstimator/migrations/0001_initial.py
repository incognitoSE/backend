# Generated by Django 3.1.7 on 2021-05-12 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Simcard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('rond', models.IntegerField(choices=[(0, 0), (1, 1)])),
                ('stock', models.IntegerField(choices=[(0, 0), (1, 1)])),
                ('daemi', models.IntegerField(choices=[(0, 0), (1, 1)])),
                ('link', models.URLField(blank=True)),
                ('price', models.IntegerField(default=-1)),
            ],
        ),
    ]
