from rest_framework.generics import GenericAPIView
from helpers.permissions import CustomDriverPermission
from apps.order.models import Trip
from rest_framework import status, response
from django.shortcuts import get_object_or_404


class DriverTripStartView(GenericAPIView):
    permission_classes = CustomDriverPermission

    def get_object(self):
        return get_object_or_404(Trip, status=Trip.TripStatus.ACTIVE, driver=self.request.user.driver)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Trip.TripStatus.IN_PROCESS
        instance.save()
        return response.Response({"Successfully started the trip"}, status=status.HTTP_200_OK)


__all__ = ['DriverTripStartView']
