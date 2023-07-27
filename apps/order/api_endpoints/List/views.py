from rest_framework.generics import ListAPIView

from apps.order.api_endpoints.List.serializers import OrderListSerializer
from apps.order.models import Order


class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer
    """
    permission_classes = IsDriver and DriverHasEnoughBalance
    """
    filterset_fields = ("pick_up_address__city",)

    def get_queryset(self):
        return Order.objects.filter(status=Order.OrderStatus.REQUESTED)


__all__ = ["OrderListView"]
