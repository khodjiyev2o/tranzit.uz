from rest_framework.generics import ListAPIView
from apps.order.models import Order
from rest_framework.permissions import IsAuthenticated
from apps.order.api_endpoints.UserOrderList.serializers import UserOrderListSerializer


class UserOrderListView(ListAPIView):
    serializer_class = UserOrderListSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client__phone="+998913665113")


__all__ = ['UserOrderListView']
