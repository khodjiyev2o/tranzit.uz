from django.db.models import Prefetch, Q
from rest_framework.generics import RetrieveAPIView

from apps.driver.api_endpoints.Trip.Retrieve.serializers import DriverTripSerializer
from apps.order.models import Order, Trip
from helpers.permissions import CustomDriverPermission


class DriverTripRetrieveView(RetrieveAPIView):
    serializer_class = DriverTripSerializer
    permission_classes = CustomDriverPermission

    def get_object(self):
        """
        Do not use get_or_create, there is no prefetch_related method with tuple object.
        Using prefetch_related is the must, as it needs to be optimized.
        """
        trip = (
            Trip.objects.filter(
                Q(status=Trip.TripStatus.ACTIVE) | Q(status=Trip.TripStatus.IN_PROCESS), driver=self.request.user.driver
            )
            .prefetch_related(
                Prefetch(
                    "client", queryset=Order.objects.select_related("pick_up_address", "drop_off_address", "client")
                ),
                Prefetch(
                    "delivery", queryset=Order.objects.select_related("pick_up_address", "drop_off_address", "client")
                ),
            )
            .select_related("driver")
            .first()
        )

        if trip is None:
            trip = Trip.objects.create(status=Trip.TripStatus.ACTIVE, driver=self.request.user.driver)
        return trip


__all__ = ["DriverTripRetrieveView"]
