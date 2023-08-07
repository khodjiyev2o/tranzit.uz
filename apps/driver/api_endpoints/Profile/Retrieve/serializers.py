from rest_framework import serializers

from apps.driver.models import Driver
from apps.users.models import User


class DriverUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "photo", "phone")


class RetrieveDriverProfileSerializer(serializers.ModelSerializer):
    user = DriverUserProfileSerializer()

    class Meta:
        model = Driver
        fields = ("id", "user", "balance")
