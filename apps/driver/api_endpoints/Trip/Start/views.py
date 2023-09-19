from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import response, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from apps.order.models import Trip
from helpers.permissions import CustomDriverPermission


class DriverTripStartView(APIView):
    permission_classes = CustomDriverPermission

    def get_object(self):
        return get_object_or_404(Trip, status=Trip.TripStatus.ACTIVE, driver=self.request.user.driver)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.client.exists() and not instance.delivery.exists():
            raise ValidationError(detail=_("No  orders found on the trip"), code="no_order_found")

        instance.status = Trip.TripStatus.IN_PROCESS
        instance.save()
        return response.Response({"message": _("Successfully started the trip")}, status=status.HTTP_200_OK)


__all__ = ["DriverTripStartView"]
