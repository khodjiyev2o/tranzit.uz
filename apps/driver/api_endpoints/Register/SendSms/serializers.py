from rest_framework import serializers


class DriverRegisterSmsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
