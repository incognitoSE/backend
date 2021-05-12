from rest_framework import serializers
from .models import Simcard


class SimcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simcard
        fields = ('id', 'number', 'rond', 'stock', 'daemi')