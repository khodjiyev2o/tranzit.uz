from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel

from .managers import UserManager


class User(AbstractUser, BaseModel):
    first_name = None
    last_name = None
    username = None
    full_name = models.CharField(_("Full Name"), max_length=255, unique=True)
    phone = models.CharField(_("Phone number"), max_length=13, unique=True)
    photo = models.ImageField(_("Photo"), upload_to="users/%Y/%m", blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []  # type: ignore

    def __str__(self):
        if self.full_name:
            return self.full_name
        if self.phone:
            return self.phone
        return "No Username"

    @property
    def tokens(self):
        token = RefreshToken.for_user(self)
        return {"access": str(token.access_token), "refresh": str(token)}

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
