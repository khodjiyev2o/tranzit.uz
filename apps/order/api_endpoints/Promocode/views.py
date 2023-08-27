from rest_framework.permissions import IsAuthenticated
from apps.common.models import Promocode
from rest_framework.generics import RetrieveAPIView
from apps.order.api_endpoints.Promocode.serializers import PromocodeRetrieveViewSerializer
from django.utils import timezone


class PromocodeRetrieveView(RetrieveAPIView):
    queryset = Promocode.objects.filter(expires_at__gte=timezone.now())
    serializer_class = PromocodeRetrieveViewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "code"
    lookup_url_kwarg = "code"


__all__ = ['PromocodeRetrieveView']
