from django.shortcuts import get_object_or_404
from rest_framework import response, status
from rest_framework.generics import GenericAPIView

from apps.order.models import Trip
from helpers.permissions import CustomDriverPermission


class DriverTripCompleteView(GenericAPIView):
    permission_classes = CustomDriverPermission

    def get_object(self):
        return get_object_or_404(Trip, status=Trip.TripStatus.IN_PROCESS, driver=self.request.user.driver)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Trip.TripStatus.COMPLETED
        instance.save()
        # need to return the overall price  and cheque
        return response.Response({"Successfully completed the trip"}, status=status.HTTP_200_OK)


__all__ = ["DriverTripCompleteView"]
