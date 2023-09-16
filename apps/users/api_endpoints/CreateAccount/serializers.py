from rest_framework import serializers
from apps.users.models import User
from rest_framework.exceptions import ValidationError


class UserCreateAccountSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, required=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        user = User.objects.filter(phone=phone).first()

        if user is not None:
            raise ValidationError(detail="User already exists", code="user_exists")

        return attrs
