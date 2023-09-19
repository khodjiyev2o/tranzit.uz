from phonenumber_field.validators import validate_international_phonenumber
from rest_framework import serializers


class DriverLoginSmsSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[validate_international_phonenumber])
