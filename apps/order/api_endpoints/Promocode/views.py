from django.utils import timezone
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.common.models import Promocode, UserPromocode
from apps.order.api_endpoints.Promocode.serializers import (
    PromocodeRetrieveViewSerializer,
)


class PromocodeRetrieveView(RetrieveAPIView):
    serializer_class = PromocodeRetrieveViewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "code"
    lookup_url_kwarg = "code"

    def get_queryset(self):
        code = self.kwargs.get("code")
        is_used = UserPromocode.objects.filter(user=self.request.user, promocode__code=code).exists()
        if is_used:
            return Promocode.objects.none()
        return Promocode.objects.filter(expires_at__gte=timezone.now(), code=code)


__all__ = ["PromocodeRetrieveView"]
