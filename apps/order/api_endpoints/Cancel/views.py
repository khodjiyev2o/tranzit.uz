from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.response import Response

from apps.order.api_endpoints.Cancel.serializers import DriverOrderCancelSerializer
from apps.order.models import Order, Trip
from helpers.permissions import CustomDriverPermission


class OrderCancelView(generics.GenericAPIView):
    serializer_class = DriverOrderCancelSerializer
    permission_classes = CustomDriverPermission

    def get_queryset(self):
        trip, _ = Trip.objects.get_or_create(status=Trip.TripStatus.ACTIVE, driver=self.request.user.driver)
        return trip

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data["order"]
        trip = self.get_queryset()

        if order.type == Order.OrderType.PERSON:
            if trip.client.filter(id=order.id).exists():
                trip.client.remove(order)  # removing from driver's trip
                order.canceled_by_driver()  # returning to the REQUESTED state
                return Response({_("Successfully removed")}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({_("Order does not exist on your trip")}, status=status.HTTP_404_NOT_FOUND)

        elif order.type == Order.OrderType.DELIVERY:
            if trip.delivery.filter(id=order.id).exists():
                trip.delivery.remove(order)
                order.canceled_by_driver()
                return Response({_("Successfully removed")}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({_("Order does not exist on your trip")}, status=status.HTTP_404_NOT_FOUND)


__all__ = ["OrderCancelView"]
