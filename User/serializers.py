from rest_framework import serializers
from .models import UserProfile, UserHistory, UserWallet


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #
    #     user = UserProfile(
    #         email=validated_data['email'],
    #         name=validated_data['name']
    #     )
    #
    #     user.set_password(validated_data['password'])
    #
    #     user.save()
    #
    #     return user


class UserhistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHistory
        fields = ("id", "data", "price", "date")


class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ("id", "amount")