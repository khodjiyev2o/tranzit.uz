from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
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
            for client in trip.client.all():
                try:
                    self.check_validation(client=client, order=order)
                except ValidationError:
                    return Response(
                        {"detail": _("Seats conflict with another order")}, status=status.HTTP_400_BAD_REQUEST
                    )

            self.update_order_state(order=order, trip_id=trip.id, order_type=Order.OrderType.PERSON)
        else:
            self.update_order_state(order=order, trip_id=trip.id, order_type=Order.OrderType.DELIVERY)

        return Response({"message": _("Order added to trip successfully.")}, status=status.HTTP_200_OK)

    @staticmethod
    def check_validation(order: Order, client: Order) -> None:
        if order.back_middle is True and order.back_middle == client.back_middle:
            raise ValidationError

        if order.front_right is True and order.front_right == client.front_right:
            raise ValidationError

        if order.back_left is True and order.back_left == client.back_left:
            raise ValidationError

        if order.back_right is True and order.back_right == client.back_right:
            raise ValidationError

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
        except Exception as e:
            raise e


__all__ = ["OrderAcceptView"]
