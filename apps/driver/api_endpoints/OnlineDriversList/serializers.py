from rest_framework import serializers
from apps.driver.models import Driver
from apps.order.models import Trip
from apps.users.models import User


class OnlineDriverListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "photo", "phone")


class OnlineDriverListDriverSerializer(serializers.ModelSerializer):
    user = OnlineDriverListUserSerializer()

    class Meta:
        model = Driver
        fields = ("id", "user", "car_number", "car_model")


class OnlineDriverListTripSerializer(serializers.ModelSerializer):
    driver = OnlineDriverListDriverSerializer()
    number_of_people = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ("id", "driver", "number_of_people", )

    def get_number_of_people(self, obj):
        return obj.client.count()
