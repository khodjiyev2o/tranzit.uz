from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.driver.api_endpoints.Profile.Image.serializers import (
    DriverPhotoUpdateSerializer,
)


class DriverPhotoUpdateView(UpdateAPIView):
    serializer_class = DriverPhotoUpdateSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user


__all__ = ["DriverPhotoUpdateView"]
