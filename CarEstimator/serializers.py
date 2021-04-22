from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'get_abs_url', 'brand', 'model', 'year', 'mileage', 'body_status')