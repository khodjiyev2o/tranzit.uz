from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.order.api_endpoints.Create.serializers import OrderCreateSerializer
from apps.order.models import Order


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


__all__ = ["OrderCreateView"]
