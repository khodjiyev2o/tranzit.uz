from rest_framework.generics import UpdateAPIView

from apps.driver.api_endpoints.Profile.Update.serializers import (
    DriverProfileUpdateSerializer,
)
from helpers.permissions import CustomDriverPermission


class DriverProfileUpdateView(UpdateAPIView):
    serializer_class = DriverProfileUpdateSerializer
    permission_classes = CustomDriverPermission

    def get_object(self):
        return self.request.user


__all__ = ["DriverProfileUpdateView"]
