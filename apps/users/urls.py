from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.api_endpoints import (
    UserCreateAccountView,
    UserDetailUpdateView,
    UserLoginSendSMSView,
)


application_urlpatterns = [
    path("retrieve-update/", UserDetailUpdateView.as_view(), name="user-retrieve-update"),
    path("create-account/", UserCreateAccountView.as_view(), name="user-create-account"),
    path("login/", UserLoginSendSMSView.as_view(), name="user-login-send-sms"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = application_urlpatterns
