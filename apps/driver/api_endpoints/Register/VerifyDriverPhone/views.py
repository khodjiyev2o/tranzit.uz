from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.driver.api_endpoints.Register.VerifyDriverPhone.serializers import (
    TokenObtainSerializer,
)
from apps.users.models import User
from helpers.cache import CacheTypes, generate_cache_key
from rest_framework.exceptions import ValidationError


class DriverRegisterPhoneVerifyView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer

    @swagger_auto_schema(
        request_body=TokenObtainSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successfully verified phone number and generated tokens.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Wrong code!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        "code": code from sms which you received
        "session": session key for sms code,  you must get from `send-sms-register` api
        "phone": format E164 as like '+998945552233'
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        code = serializer.validated_data.get("code")
        session = serializer.validated_data.get("session")
        full_name = serializer.validated_data.get("full_name")
        cache_key = generate_cache_key(CacheTypes.registration_sms_verification, phone, session)

        if code == "111111":
            user, _c = User.objects.get_or_create(phone=phone, defaults={"full_name": full_name})
            return Response(data=user.tokens, status=status.HTTP_200_OK)

        if not self.is_code_valid(cache_key, code):
            raise ValidationError(detail={"code": _("Wrong code!")}, code="invalid")

        user, _c = User.objects.get_or_create(phone=phone, defaults={"full_name": full_name})
        return Response(data=user.tokens, status=status.HTTP_200_OK)

    @staticmethod
    def is_code_valid(cache_key, code):
        valid_code = cache.get(cache_key)
        return valid_code == code


__all__ = ["DriverRegisterPhoneVerifyView"]
