from rest_framework import serializers


class DriverLoginSmsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
