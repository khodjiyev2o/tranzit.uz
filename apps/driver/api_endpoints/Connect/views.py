from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.permissions import IsDriver


class DriverOnlineStateView(APIView):
    permission_classes = [IsDriver]

    def get_object(self):
        return self.request.user.driver

    def put(self, request, *args, **kwargs):
        # Get the driver object
        driver = self.get_object()

        # Toggle the online status
        driver.is_online = True
        driver.save()

        return Response({"success": True, "is_online": driver.is_online}, status=status.HTTP_200_OK)


class DriverOfflineStateView(APIView):
    permission_classes = [IsDriver]

    def get_object(self):
        return self.request.user.driver

    def put(self, request, *args, **kwargs):
        # Get the driver object
        driver = self.get_object()

        # Toggle the online status
        driver.is_online = False
        driver.save()

        return Response({"success": True, "is_online": driver.is_online}, status=status.HTTP_200_OK)
