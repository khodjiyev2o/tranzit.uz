from rest_framework import serializers

from apps.driver.models import Driver
from apps.order.models import Order, Trip


class DriverSerializerForTrip(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("has_air_conditioner", "has_baggage", "smoking_allowed")


class DriverTripClientSerializer(serializers.ModelSerializer):
    seats = serializers.SerializerMethodField()
    client = serializers.CharField(source="client.full_name")

    class Meta:
        model = Order
        fields = ("id", "client", "price", "seats", "approximate_leave_time")

    def get_seats(self, obj):
        chosen_seats = []
        if obj.front_right is True:
            chosen_seats.append("front_right")
        if obj.back_left is True:
            chosen_seats.append("back_left")
        if obj.back_middle is True:
            chosen_seats.append("back_middle")
        if obj.back_right is True:
            chosen_seats.append("back_right")
        return chosen_seats


class DriverTripDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "delivery_user_phone", "delivery_type", "price", "approximate_leave_time")


class DriverTripSerializer(serializers.ModelSerializer):
    driver = DriverSerializerForTrip()
    client = DriverTripClientSerializer(many=True)
    delivery = DriverTripDeliverySerializer(many=True)

    class Meta:
        model = Trip
        fields = ("id", "driver", "client", "delivery")
