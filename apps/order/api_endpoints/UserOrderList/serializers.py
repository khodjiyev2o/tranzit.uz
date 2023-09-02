from rest_framework import serializers
from apps.order.models import Order, Driver, Location


class UserOrderDriverSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="user.phone")

    class Meta:
        model = Driver
        fields = ("phone", )


class UserOrderLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ("id", "created_at", "updated_at")


class UserOrderListSerializer(serializers.ModelSerializer):
    driver = UserOrderDriverSerializer()
    drop_off_address = UserOrderLocationSerializer()
    pick_up_address = UserOrderLocationSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "driver",
            "approximate_leave_time",
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
