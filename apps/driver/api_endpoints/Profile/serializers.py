from rest_framework import serializers

from apps.driver.models import Driver
from apps.users.models import User


class DriverUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "photo", "phone")
        extra_kwargs = {"phone": {"read_only": True}}


class RetrieveUpdateDriverProfileSerializer(serializers.ModelSerializer):
    user = DriverUserProfileSerializer()

    class Meta:
        model = Driver
        fields = ("id", "user", "balance")
        extra_kwargs = {
            "id": {"read_only": True},
            "balance": {"read_only": True},
        }
