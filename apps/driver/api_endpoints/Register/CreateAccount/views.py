from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.driver.api_endpoints.Register.CreateAccount.serializers import (
    CreateDriverAccountSerializer,
)
from apps.driver.models import Driver


class CreateDriverAccountView(CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = CreateDriverAccountSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


__all__ = ["CreateDriverAccountView"]
