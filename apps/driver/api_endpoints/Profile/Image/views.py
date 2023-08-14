from rest_framework.generics import UpdateAPIView

from apps.driver.api_endpoints.Profile.Image.serializers import (
    DriverPhotoUpdateSerializer,
)
from helpers.permissions import IsDriver


class DriverPhotoUpdateView(UpdateAPIView):
    serializer_class = DriverPhotoUpdateSerializer
    permission_classes = [IsDriver, ]

    def get_object(self):
        return self.request.user


__all__ = ["DriverPhotoUpdateView"]
