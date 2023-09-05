from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.order.api_endpoints.UserOrderCancel.serializers import (
    UserOrderCancelSerializer,
)
from apps.order.models import Order
from rest_framework.response import Response


class UserOrderCancelView(GenericAPIView):
    serializer_class = UserOrderCancelSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data["order"]

        order.status = Order.OrderStatus.CANCELED
        order.save()

        return Response({"message": "Canceled successfully!"}, status=200)


__all__ = ["UserOrderCancelView"]
