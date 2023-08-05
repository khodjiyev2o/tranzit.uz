from rest_framework.generics import ListAPIView

from apps.order.api_endpoints.List.serializers import OrderListSerializer
from apps.order.models import Order
from helpers.permissions import CustomDriverPermission


class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = CustomDriverPermission
    filterset_fields = ("pick_up_address__city",)

    def get_queryset(self):
        return Order.objects.filter(status=Order.OrderStatus.REQUESTED).select_related(
            "client", "pick_up_address", "drop_off_address"
        )


__all__ = ["OrderListView"]
