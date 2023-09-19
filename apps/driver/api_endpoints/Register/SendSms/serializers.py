from rest_framework import serializers
from phonenumber_field.validators import validate_international_phonenumber


class DriverRegisterSmsSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[validate_international_phonenumber])
