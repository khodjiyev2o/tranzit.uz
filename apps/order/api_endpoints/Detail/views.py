from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.order.api_endpoints.Detail.serializers import OrderDetailSerializer
from apps.order.models import Order


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Order.objects.filter(id=self.kwargs.get("pk")).select_related("client", "pick_up_address").first()


__all__ = ["OrderDetailView"]
