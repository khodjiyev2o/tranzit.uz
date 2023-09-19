from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.order.models import Order


class DriverOrderCancelSerializer(serializers.Serializer):
    order = serializers.IntegerField()

    def validate_order(self, order_id):
        try:
            order = Order.objects.get(pk=order_id, status=Order.OrderStatus.IN_PROGRESS)
        except Order.DoesNotExist:
            raise serializers.ValidationError(
                detail={"order": _("Order not found or already taken by another driver.")},
                code="not_found"
            )

        return order
