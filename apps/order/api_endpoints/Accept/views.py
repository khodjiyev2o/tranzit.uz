from django.db.models import Q, Sum
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.response import Response

from apps.order.api_endpoints.Accept.serializers import DriverOrderAcceptSerializer
from apps.order.models import Order, Trip
from helpers.permissions import CustomDriverPermission


class OrderAcceptView(generics.GenericAPIView):
    serializer_class = DriverOrderAcceptSerializer
    permission_classes = CustomDriverPermission

    def get_queryset(self):
        trip, _ = Trip.objects.get_or_create(status=Trip.TripStatus.ACTIVE, driver=self.request.user.driver)
        return trip

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data["order_id"]
        trip = self.get_queryset()

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.type == Order.OrderType.PERSON:
            # Check if the order's seats conflict with other orders
            conflicting_seats = trip.client.filter(
                Q(front_right=order.front_right)
                | Q(back_left=order.back_left)
                | Q(back_middle=order.back_middle)
                | Q(back_right=order.back_right)
            ).exists()
            if conflicting_seats:
                return Response({"detail": "Seats conflict with another order"}, status=status.HTTP_400_BAD_REQUEST)

            trip.client.add(order)
        else:
            trip.delivery.add(order)

        return Response({"message": _("Order added to trip successfully.")}, status=status.HTTP_200_OK)


__all__ = ["OrderAcceptView"]
