from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.order.api_endpoints.UserOrderList.serializers import UserOrderListSerializer
from apps.order.models import Order


class UserOrderListView(ListAPIView):
    serializer_class = UserOrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)


__all__ = ["UserOrderListView"]
