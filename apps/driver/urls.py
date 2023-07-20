from django.urls import path

from apps.driver.api_endpoints import DriverRegisterPhoneVerifyView, DriverRegisterSendSMSView


urlpatterns = [
    path("register/send-sms/", DriverRegisterSendSMSView.as_view(), name="driver-register-send-sms"),
    path("register/verify-phone/", DriverRegisterPhoneVerifyView.as_view(), name="driver-register-verify-phone"),
]
