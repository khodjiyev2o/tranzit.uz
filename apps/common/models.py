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

    def is_used_by_user(self, user):
        # Check if the promocode is used by the given user
        return self.user_promocode.filter(user=user).exists()

    def __str__(self):
        return str(self.code)


class UserPromocode(BaseModel):
    promocode = models.ForeignKey(
        Promocode, on_delete=models.CASCADE, verbose_name=_("Promocode"), related_name="user_promocode"
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("User"))

    class Meta:
        verbose_name = _("UserPromocode")
        verbose_name_plural = _("UserPromocodes")
        db_table = "user_promocode"
        ordering = ("-id",)


class FrontTranslation(models.Model):
    key = models.CharField(max_length=511, verbose_name=_("Key"), unique=True)
    text = models.TextField(verbose_name=_("Text"))

    class Meta:
        db_table = "front_translation"
        verbose_name = _("Front Translation")
        verbose_name_plural = _("Front Translations")

    def __str__(self):
        return f"{self.key}"
