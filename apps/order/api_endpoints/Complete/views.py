from rest_framework.generics import GenericAPIView
from helpers.permissions import CustomDriverPermission
from apps.order.models import Trip
from rest_framework import status, response
from django.shortcuts import get_object_or_404


class DriverTripCompleteView(GenericAPIView):
    permission_classes = CustomDriverPermission

    def get_object(self):
        return get_object_or_404(Trip, status=Trip.TripStatus.IN_PROCESS, driver=self.request.user.driver)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Trip.TripStatus.COMPLETED
        instance.save()
        #need to return the overall price  and cheque
        return response.Response({"Successfully completed the trip"}, status=status.HTTP_200_OK)


__all__ = ['DriverTripCompleteView']
