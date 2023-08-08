from rest_framework.generics import RetrieveAPIView

from apps.driver.api_endpoints.Trip.Retrieve.serializers import DriverTripSerializer
from apps.order.models import Trip
from helpers.permissions import CustomDriverPermission


class DriverTripRetrieveView(RetrieveAPIView):
    serializer_class = DriverTripSerializer
    permission_classes = CustomDriverPermission

    def get_object(self):
        trip, _ = Trip.objects.get_or_create(status=Trip.TripStatus.ACTIVE, driver=self.request.user.driver)
        return trip


__all__ = ["DriverTripRetrieveView"]
