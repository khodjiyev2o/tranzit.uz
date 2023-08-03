from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.driver.api_endpoints.Status.serializers import DriverStatusSerializer
from helpers.permissions import IsDriver


class DriverStatusView(RetrieveAPIView):
    serializer_class = DriverStatusSerializer
    permission_classes = [IsAuthenticated, IsDriver]

    def get_object(self):
        return self.request.user.driver


__all__ = ["DriverStatusView"]
