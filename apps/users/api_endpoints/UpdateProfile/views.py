from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.api_endpoints.UpdateProfile.serializers import (
    UserRetrieveUpdateSerializer,
)


class UserDetailUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


__all__ = ["UserDetailUpdateView"]
