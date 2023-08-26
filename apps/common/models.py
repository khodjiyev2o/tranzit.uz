from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class Promocode(BaseModel):
    code = models.CharField(max_length=255, verbose_name=_("Code"), unique=True)
    expires_at = models.DateTimeField(_("Expired at"))
    max_usage_count = models.IntegerField(default=100, verbose_name=_("Maximum Usage Count"))
    money_amount = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Promocode")
        verbose_name_plural = _("Promocodes")
        db_table = "promocode"
        ordering = ("-id",)


class UserPromocode(BaseModel):
    promocode = models.ForeignKey(Promocode, on_delete=models.CASCADE, verbose_name=_("Promocode"))
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("User"))

    class Meta:
        verbose_name = _("UserPromocode")
        verbose_name_plural = _("UserPromocodes")
        db_table = "user_promocode"
        ordering = ("-id",)
