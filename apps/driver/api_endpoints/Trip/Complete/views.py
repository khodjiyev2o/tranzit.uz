from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import response, status
from rest_framework.views import APIView

from apps.order.models import Order, Trip
from helpers.permissions import CustomDriverPermission


class DriverTripCompleteView(APIView):
    permission_classes = CustomDriverPermission

    def get_object(self):
        return get_object_or_404(Trip, status=Trip.TripStatus.IN_PROCESS, driver=self.request.user.driver)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        # taking fee only for clients, ** delivery is free
        amount_to_be_taken = int(instance.total_amount_from_client * settings.TRANSIT_SERVICE_FEE)
        promocode_amount = instance.total_amount_promo_code

        self.update_driver_balance_and_trip_state(
            trip=instance, amount=amount_to_be_taken, promocode_amount=promocode_amount
        )
        return response.Response(
            {
                "message": "Successfully completed the trip",
                "total_amount": instance.total_amount_from_delivery + instance.total_amount_from_client,
                "amount_to_be_taken": amount_to_be_taken,
                "promocode_amount": promocode_amount,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @transaction.atomic
    def update_driver_balance_and_trip_state(trip: Trip, amount: int, promocode_amount: int) -> None:
        try:
            # charging service fee from driver
            driver = trip.driver
            driver.balance -= amount
            driver.balance += promocode_amount
            driver.save()

            # making the trip state COMPLETED
            trip.status = Trip.TripStatus.COMPLETED
            trip.save()

            # making the orders state of the trip COMPLETED
            trip.client.update(status=Order.OrderStatus.COMPLETED)
            trip.delivery.update(status=Order.OrderStatus.COMPLETED)

        except Exception as e:
            raise e


__all__ = ["DriverTripCompleteView"]
