from rest_framework import serializers

from apps.order.models import Location, Order, User


class LocationOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ("id", "created_at", "updated_at")


class ClientOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "phone")


class OrderDetailSerializer(serializers.ModelSerializer):
    client = ClientOrderDetailSerializer()

    pick_up_address = LocationOrderDetailSerializer()
    drop_off_address = LocationOrderDetailSerializer()

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
            "delivery_type",
        )
