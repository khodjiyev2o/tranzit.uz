from rest_framework import serializers


class DriverOrderAcceptSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
