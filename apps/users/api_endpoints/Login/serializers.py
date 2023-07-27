from rest_framework import serializers


class UserLoginSmsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
