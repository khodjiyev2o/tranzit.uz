from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.response import Response

from apps.order.api_endpoints.Accept.serializers import DriverOrderAcceptSerializer
from apps.order.models import Order, Trip
from helpers.permissions import CustomDriverPermission
from django.db import transaction


class OrderAcceptView(generics.GenericAPIView):
    serializer_class = DriverOrderAcceptSerializer
    permission_classes = CustomDriverPermission

    def get_queryset(self):
        trip, _ = Trip.objects.get_or_create(status=Trip.TripStatus.ACTIVE, driver=self.request.user.driver)
        return trip

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data["order"]
        trip = self.get_queryset()

        for previous_client_order in trip.client.all():
            if previous_client_order.pick_up_address.city != order.pick_up_address.city:
                return Response(
                    {"detail": _("All client orders and deliveries should have the same pick-up address.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        for delivery in trip.delivery.all():  # pragma: no cover
            if delivery.pick_up_address.city != order.pick_up_address.city:
                return Response(
                    {"detail": _("All client orders and deliveries should have the same pick-up address.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if order.type == Order.OrderType.PERSON:
            # Check if the order's seats conflict with other orders
            conflicting_seats = trip.client.filter(
                Q(front_right=order.front_right)
                | Q(back_left=order.back_left)
                | Q(back_middle=order.back_middle)
                | Q(back_right=order.back_right)
            ).exists()
            if conflicting_seats:
                return Response({"detail": _("Seats conflict with another order")}, status=status.HTTP_400_BAD_REQUEST)

            self.update_order_state(order=order, trip_id=trip.id, order_type=Order.OrderType.PERSON)
        else:
            self.update_order_state(order=order, trip_id=trip.id, order_type=Order.OrderType.DELIVERY)

        return Response({"message": _("Order added to trip successfully.")}, status=status.HTTP_200_OK)

    @staticmethod
    @transaction.atomic
    def update_order_state(order: Order, trip_id: int, order_type: str):
        try:
            trip = Trip.objects.get(id=trip_id)
            if order_type == Order.OrderType.PERSON:
                trip.client.add(order)
            else:
                trip.delivery.add(order)

            order.taken_by_driver()
            # Additional processing related to the transaction
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e


__all__ = ["OrderAcceptView"]

