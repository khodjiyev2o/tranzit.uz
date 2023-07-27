from rest_framework import serializers

from apps.users.models import User


class UserCreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone",)
