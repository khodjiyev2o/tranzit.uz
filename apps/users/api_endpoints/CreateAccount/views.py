from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_409_CONFLICT
from rest_framework.views import APIView

from apps.driver.models import Driver
from apps.users.api_endpoints.CreateAccount.serializers import (
    UserCreateAccountSerializer,
)
from apps.users.api_endpoints.utils import CacheTypes


class CreateAccountView(APIView):
    @swagger_auto_schema(
        request_body=UserCreateAccountSerializer,
        operation_description="""
            email:  as like ' samandarkhodjiyev@gmail.com '
        """,
    )
    def post(self, request, *args, **kwargs):
        serializer = UserCreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check if driver account already exists
        if self.driver_exists(request):
            return Response(
                {"success": False, "message": _("Driver account already exists!")}, status=HTTP_409_CONFLICT
            )

        phone = serializer.validated_data.get("phone")
        session = get_random_string(length=16)

        # check if SMS was sent to this email  within 2 minutes for login or registration
        cache_keys = cache.keys(f"{CacheTypes.registration_sms_verification}{str(phone)}*")
        if cache_keys:
            raise ValidationError(detail={"phone": _("SMS is already sent!")}, code="timeout")

        # send 6 digits code to phone
        return Response({"session": session})

    @staticmethod
    def driver_exists(request):
        try:
            Driver.objects.get(user__phone=request.data.get("phone"), user__full_name=request.data.get("full_name"))
            return True
        except Driver.DoesNotExist:
            return False


__all__ = ["CreateAccountView"]