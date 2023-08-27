from rest_framework import serializers
from apps.order.models import Order


class GeneratePriceSerializer(serializers.ModelSerializer):
    pick_up_city = serializers.CharField(source="pick_up_address.city")
    drop_off_city = serializers.CharField(source="drop_off_address.city")

    class Meta:
        model = Order
        fields = (
            "pick_up_city",
            "drop_off_city",
            "number_of_people",
            "front_right",
            "back_left",
            "back_middle",
            "back_right",
        )
