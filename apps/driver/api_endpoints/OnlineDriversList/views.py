from rest_framework.generics import ListAPIView
from apps.driver.models import Driver, DriverStatus
from apps.order.models import Trip
from rest_framework.permissions import IsAuthenticated
from apps.driver.api_endpoints.OnlineDriversList.serializers import OnlineDriverListTripSerializer


class OnlineDriverListView(ListAPIView):
    queryset = Trip.objects.filter(driver__is_online=True, driver__status=DriverStatus.ACTIVE, status=Trip.TripStatus.ACTIVE)
    serializer_class = OnlineDriverListTripSerializer
    permission_classes = [IsAuthenticated, ]


__all__ = ['OnlineDriverListView']
