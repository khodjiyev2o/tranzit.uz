from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from apps.common.utils import send_activation_code_via_sms
from apps.driver.api_endpoints.Login.SendSMS.serializers import DriverLoginSmsSerializer
from apps.driver.models import Driver
from helpers.cache import CacheTypes


class DriverLoginSendSMSView(GenericAPIView):
    serializer_class = DriverLoginSmsSerializer

    @swagger_auto_schema(
        request_body=DriverLoginSmsSerializer,
        operation_description="""
            phone:  as like '+998913665113'
        """,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check if driver account already exists
        if not self.driver_exists(request):
            raise ValidationError(detail={"driver": _("Driver not found!")}, code="not_found")

        phone = serializer.validated_data.get("phone")
        session = get_random_string(length=16)

        # check if SMS was sent to this phone  within 2 minutes for login or registration
        cache_keys = cache.keys(f"{CacheTypes.registration_sms_verification}{str(phone)}*")
        if cache_keys:
            raise ValidationError(detail={"phone": _("SMS is already sent!")}, code="timeout")

        # send 6 digits code to phone
        send_activation_code_via_sms(str(phone), CacheTypes.registration_sms_verification, session)
        return Response({"session": session})

    @staticmethod
    def driver_exists(request):
        try:
            Driver.objects.get(user__phone=request.data.get("phone"))
            return True
        except Driver.DoesNotExist:
            return False


__all__ = ["DriverLoginSendSMSView"]
