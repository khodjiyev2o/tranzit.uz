from rest_framework import serializers

from apps.users.models import User


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "photo", "phone")
        extra_kwargs = {"phone": {"read_only": True}}
