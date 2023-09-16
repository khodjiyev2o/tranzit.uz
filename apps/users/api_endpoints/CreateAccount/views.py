from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.common.utils import send_activation_code_via_sms

from apps.users.api_endpoints.CreateAccount.serializers import (
    UserCreateAccountSerializer,
)
from helpers.cache import CacheTypes


class UserCreateAccountView(APIView):
    @swagger_auto_schema(
        request_body=UserCreateAccountSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = UserCreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get("phone")
        session = get_random_string(length=16)

        # check if SMS was sent to this email  within 2 minutes for login or registration
        cache_keys = cache.keys(f"{CacheTypes.registration_sms_verification}{str(phone)}*")
        if cache_keys:
            raise ValidationError(detail={"phone": _("SMS is already sent!")}, code="timeout")

        # send 6 digits code to phone
        send_activation_code_via_sms(str(phone), CacheTypes.registration_sms_verification, session)

        return Response({"session": session})


__all__ = ["UserCreateAccountView"]
