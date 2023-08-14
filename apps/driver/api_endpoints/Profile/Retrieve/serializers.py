from rest_framework import serializers

from apps.driver.models import Driver
from apps.users.models import User
from django.conf import settings


class DriverUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "photo", "phone")


class RetrieveDriverProfileSerializer(serializers.ModelSerializer):
    user = DriverUserProfileSerializer()
    minimum_balance = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ("id", "user", "balance", "minimum_balance")

    def get_minimum_balance(self, obj):
        return settings.TRANSIT_DRIVER_MINIMUM_BALANCE
