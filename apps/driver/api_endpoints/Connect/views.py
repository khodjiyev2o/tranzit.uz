# chat/views.py
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from helpers.permissions import IsDriver


class DriverOnlineStateView(UpdateAPIView):
    permission_classes = [IsDriver]

    def get_object(self):
        return self.request.user.driver

    def update(self, request, *args, **kwargs):
        # Get the driver object
        driver = self.get_object()

        # Toggle the online status
        driver.is_online = True
        driver.save()

        return Response({"success": True, "is_online": driver.is_online}, status=status.HTTP_200_OK)


class DriverOfflineStateView(UpdateAPIView):
    permission_classes = [IsDriver]

    def get_object(self):
        return self.request.user.driver

    def update(self, request, *args, **kwargs):
        # Get the driver object
        driver = self.get_object()

        # Toggle the online status
        driver.is_online = False
        driver.save()

        return Response({"success": True, "is_online": driver.is_online}, status=status.HTTP_200_OK)


def index(request):
    return render(request, "order/main.html")
