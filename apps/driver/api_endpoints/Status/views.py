from rest_framework.generics import RetrieveAPIView

from apps.driver.api_endpoints.Status.serializers import DriverStatusSerializer
from helpers.permissions import IsDriver


class DriverStatusView(RetrieveAPIView):
    serializer_class = DriverStatusSerializer
    permission_classes = [IsDriver]

    def get_object(self):
        return self.request.user.driver


__all__ = ["DriverStatusView"]
