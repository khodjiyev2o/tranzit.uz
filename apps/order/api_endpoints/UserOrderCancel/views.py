from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.order.api_endpoints.UserOrderCancel.serializers import (
    UserOrderCancelSerializer,
)
from apps.order.models import Order, Trip


class UserOrderCancelView(GenericAPIView):
    serializer_class = UserOrderCancelSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data["order"]

        if order.type == Order.OrderType.PERSON:

            trip = Trip.objects.filter(client=order, status=Trip.TripStatus.ACTIVE).first()
            if trip is not None:
                trip.client.remove(order)
            else:
                raise ValidationError(detail="Trip not found", code="trip_does_not_exist")
        elif order.type == Order.OrderType.DELIVERY:
            trip = Trip.objects.filter(delivery=order, status=Trip.TripStatus.ACTIVE).first()
            if trip is not None:
                trip.delivery.remove(order)
            else:
                raise ValidationError(detail="Trip not found", code="trip_does_not_exist")

        order.status = Order.OrderStatus.CANCELED
        order.save()
        return Response({"message": "Canceled successfully!"}, status=200)


__all__ = ["UserOrderCancelView"]
