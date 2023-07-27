from django.urls import path

from apps.driver.api_endpoints import (
    CreateDriverAccountView,
    DriverLoginSendSMSView,
    DriverOfflineStateView,
    DriverOnlineStateView,
    DriverRegisterPhoneVerifyView,
    DriverRegisterSendSMSView,
)


urlpatterns = [
    path("register/send-sms/", DriverRegisterSendSMSView.as_view(), name="driver-register-send-sms"),
    path("register/verify-phone/", DriverRegisterPhoneVerifyView.as_view(), name="driver-register-verify-phone"),
    path("register/create-account/", CreateDriverAccountView.as_view(), name="driver-create-account"),
    path("login/send-sms/", DriverLoginSendSMSView.as_view(), name="driver-login-send-sms"),
    path("online-status/", DriverOnlineStateView.as_view(), name="driver-online-status"),
    path("offline-status/", DriverOfflineStateView.as_view(), name="driver-offline-status"),
]
