from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.api_endpoints.UpdateProfile.serializers import (
    UserRetrieveUpdateSerializer,
)
from apps.users.models import User


class UserDetailUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserRetrieveUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


__all__ = ["UserDetailUpdateView"]