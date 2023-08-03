from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from apps.driver.models import DriverStatus
from apps.users.models import User


class IsDriver(permissions.BasePermission):
    message = _("User is not a driver")

    def has_permission(self, request, view):
        try:
            if request.user.driver:
                return True
        except User.driver.RelatedObjectDoesNotExist:
            return False


class IsActiveDriver(permissions.BasePermission):
    message = _("Driver is in moderation")

    def has_permission(self, request, view):
        return request.user.driver.status == DriverStatus.ACTIVE


class DriverHasEnoughBalance(permissions.BasePermission):
    message = _("Driver does not have enough balance")

    def has_permission(self, request, view):
        """
        30000 so'm is because average cheque of client is 6000, and 4 clients will be 24000
        """
        return request.user.driver.balance > 30000


CustomDriverPermission = [IsAuthenticated, IsDriver, IsActiveDriver, DriverHasEnoughBalance]
