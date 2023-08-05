from rest_framework.generics import RetrieveAPIView

from apps.driver.api_endpoints.Trip.serializers import DriverTripSerializer
from apps.order.models import Trip
from helpers.permissions import CustomDriverPermission


class DriverTripRetrieveView(RetrieveAPIView):
    serializer_class = DriverTripSerializer
    permission_classes = CustomDriverPermission

    def get_object(self):
        return Trip.objects.filter(status=Trip.TripStatus.ACTIVE, driver=self.request.user.driver).first()


__all__ = ["DriverTripRetrieveView"]
