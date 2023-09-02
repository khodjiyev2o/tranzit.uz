from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.order.models import Order


class UserOrderCancelSerializer(serializers.Serializer):
    order = serializers.IntegerField()

    def validate_order(self, order_id):
        try:
            order = Order.objects.get(pk=order_id, status=Order.OrderStatus.REQUESTED)
        except Order.DoesNotExist:
            raise serializers.ValidationError(_("Active Orders not found"))

        return order
