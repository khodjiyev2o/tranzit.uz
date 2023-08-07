from rest_framework import serializers

from apps.users.models import User


class DriverProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "full_name",
            "photo",
        )
