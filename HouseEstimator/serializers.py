from rest_framework import serializers
from .models import House


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'area', 'room', 'year', 'location')