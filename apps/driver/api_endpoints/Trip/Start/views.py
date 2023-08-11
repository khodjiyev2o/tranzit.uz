from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import response, status
from rest_framework.generics import GenericAPIView

from apps.order.models import Trip
from helpers.permissions import CustomDriverPermission


class DriverTripStartView(GenericAPIView):
    permission_classes = CustomDriverPermission

    def get_object(self):
        return get_object_or_404(Trip, status=Trip.TripStatus.ACTIVE, driver=self.request.user.driver)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.client.exists() and not instance.delivery.exists():
            return response.Response({"message": _("No  orders found on the trip")}, status=status.HTTP_404_NOT_FOUND)
        instance.status = Trip.TripStatus.IN_PROCESS
        instance.save()
        return response.Response({"message": _("Successfully started the trip")}, status=status.HTTP_200_OK)


__all__ = ["DriverTripStartView"]
