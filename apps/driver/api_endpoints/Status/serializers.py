from rest_framework.serializers import ModelSerializer

from apps.driver.models import Driver


class DriverStatusSerializer(ModelSerializer):
    class Meta:
        model = Driver
        fields = ("status",)
