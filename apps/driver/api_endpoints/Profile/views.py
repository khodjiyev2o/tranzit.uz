from rest_framework import generics
from rest_framework.parsers import JSONParser, MultiPartParser

from apps.driver.api_endpoints.Profile.serializers import (
    RetrieveUpdateDriverProfileSerializer,
)
from helpers.permissions import IsDriver


class DriverRetrieveUpdateProfileView(generics.RetrieveUpdateAPIView):
    """
    Update profile information. Authentication is required!
    Send the data in  form-data format if you want to change the photo.
    """

    serializer_class = RetrieveUpdateDriverProfileSerializer
    permission_classes = (IsDriver,)
    parser_classes = (MultiPartParser, JSONParser)

    def get_object(self):
        return self.request.user.driver


__all__ = ["DriverRetrieveUpdateProfileView"]
