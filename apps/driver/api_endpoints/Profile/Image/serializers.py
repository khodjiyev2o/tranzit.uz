from rest_framework import serializers

from apps.users.models import User


class DriverPhotoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("photo",)
        extra_kwargs = {"photo": {"required": True}}
