from rest_framework import serializers
from .models import House


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'get_abs_url', 'area', 'room_number', 'year', 'neighbourhood')