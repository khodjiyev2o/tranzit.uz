from django.db.models import Q
from rest_framework import serializers

from apps.order.models import Driver, Location, Order, Trip


class UserOrderDriverSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="user.phone")

    class Meta:
        model = Driver
        fields = ("phone",)


class UserOrderLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ("id", "created_at", "updated_at")


class UserOrderListSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField()
    drop_off_address = UserOrderLocationSerializer()
    pick_up_address = UserOrderLocationSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "driver",
            "status",
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

    def get_driver(self, obj):
        # Check if the order has a driver in person_orders
        if obj.person_orders.exists():
            return UserOrderDriverSerializer(obj.person_orders.first().driver).data

        # Check if the order has a driver in deliveries
        if obj.deliveries.exists():
            return UserOrderDriverSerializer(obj.deliveries.first().driver).data

        # If neither person_orders nor deliveries have a driver, return None
        return None
