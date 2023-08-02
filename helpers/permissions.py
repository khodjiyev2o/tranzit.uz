from django.utils.translation import gettext_lazy as _
from rest_framework import permissions

from apps.users.models import User


class IsDriver(permissions.BasePermission):
    message = _("User is not a driver")

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            if request.user.driver:
                return True
        except User.driver.RelatedObjectDoesNotExist:
            return False


class DriverHasEnoughBalance(permissions.BasePermission):
    message = _("Driver does not have enough balance")

    def has_permission(self, request, view):
        return request.user.driver.balance > 1000
