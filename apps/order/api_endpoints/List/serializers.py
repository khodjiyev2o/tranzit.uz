from rest_framework import serializers

from apps.order.models import Location, Order, User


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ("id", "created_at", "updated_at")


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "phone")


class OrderListSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    pick_up_address = LocationSerializer()
    drop_off_address = LocationSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "approximate_leave_time",
            "client",
            "number_of_people",
            "front_right",
            "back_left",
            "back_middle",
            "back_right",
            "pick_up_address",
            "drop_off_address",
            "price",
            "type",
            "delivery_user_phone",
        )
