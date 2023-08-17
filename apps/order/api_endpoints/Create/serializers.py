from rest_framework import serializers

from apps.order.api_endpoints.List.serializers import LocationSerializer
from apps.order.models import Location, Order


class OrderCreateSerializer(serializers.ModelSerializer):
    pick_up_address = LocationSerializer()
    drop_off_address = LocationSerializer()

    class Meta:
        model = Order
        fields = (
            "pick_up_address",
            "drop_off_address",
            "car_category",
            "price",
            "number_of_people",
            "front_right",
            "back_left",
            "back_middle",
            "back_right",
            "type",
            "delivery_user_phone",
            "delivery_type",
            "approximate_leave_time",
            "comment",
            "has_air_conditioner",
            "has_baggage",
            "smoking_allowed",
            "promocode",
        )

    def create(self, validated_data):
        pick_up_address_data = validated_data.pop("pick_up_address")
        drop_off_address_data = validated_data.pop("drop_off_address")

        pick_up_address = Location.objects.create(**pick_up_address_data)
        drop_off_address = Location.objects.create(**drop_off_address_data)

        return Order.objects.create(
            pick_up_address=pick_up_address, drop_off_address=drop_off_address, **validated_data
        )
