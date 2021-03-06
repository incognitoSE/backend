# Generated by Django 3.1.7 on 2021-05-25 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_auto_20210523_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('ch', 'افزایش اعتبار'), ('se', 'استفاده از سرویس')], max_length=100)),
                ('service', models.CharField(default='-', max_length=150)),
                ('amount', models.IntegerField()),
                ('date', models.CharField(max_length=40)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
