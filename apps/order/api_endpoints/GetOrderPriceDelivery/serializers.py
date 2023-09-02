from rest_framework import serializers
from apps.order.models import Order


class GetDeliveryOrderPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "delivery_type",
        )
