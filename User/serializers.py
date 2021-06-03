from abc import ABC

from rest_framework import serializers
from .models import UserProfile, UserHistory, UserWallet, UserTransactions, Notifications


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


class UserTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransactions
        fields = ("id", "type", "service", "amount", "date")


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ("id", "text", "date")


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'password')