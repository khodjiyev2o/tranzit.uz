from rest_framework import generics

from apps.driver.api_endpoints.Profile.Retrieve.serializers import (
    RetrieveDriverProfileSerializer,
)
from helpers.permissions import IsDriver


class DriverRetrieveProfileView(generics.RetrieveAPIView):
    """
    Retrieve profile information. Authentication is required!
    """

    serializer_class = RetrieveDriverProfileSerializer
    permission_classes = (IsDriver,)

    def get_object(self):
        return self.request.user.driver


__all__ = ["DriverRetrieveProfileView"]
