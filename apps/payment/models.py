import base64

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Provider(models.TextChoices):
    PAYME = "payme", _("Payme")
    CLICK = "click", _("Click")
    KARMON_PAY = "karmon_pay", _("Karmon Pay")
    UZUM_BANK = "uzum_bank", _("Uzum Bank")
    CARD = "card", _("Card")


class TransactionStatus(models.TextChoices):
    WAITING = "waiting", _("Waiting")
    PAID = "paid", _("Paid")
    FAILED = "failed", _("Failed")
    CANCELED = "canceled", _("Canceled")


class Order(BaseModel):
    driver = models.ForeignKey("driver.Driver", on_delete=models.CASCADE, verbose_name=_("Driver"))
    provider = models.CharField(max_length=63, verbose_name=_("Provider"), choices=Provider.choices)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"))
    is_paid = models.BooleanField(default=False, verbose_name=_("Is Paid"))
    is_canceled = models.BooleanField(default=False, verbose_name=_("Is Canceled"))

    def __str__(self):
        return f"{self.driver} - {self.total_amount}"

    @property
    def transaction_amount(self):
        return self.total_amount

    def get_payment_url(self):
        payment_url = ""
        if self.provider == Provider.PAYME:
            base_url = "https://checkout.paycom.uz"
            merchant_id = settings.PROVIDERS["payme"]["merchant_id"]
            params = (
                f"m={merchant_id};ac.phone_number={self.driver.user.phone};a=0;c=https://transitgroup.uz"
            )
            encode_params = base64.b64encode(params.encode("utf-8"))
            encode_params = str(encode_params, "utf-8")
            payment_url = f"{base_url}/{encode_params}"
        elif self.provider == Provider.CLICK:
            url = settings.PROVIDERS["click"]["url"]  # noqa
            merchant_id = settings.PROVIDERS["click"]["merchant_id"]
            service_id = settings.PROVIDERS["click"]["merchant_service_id"]
            params = (
                f"?service_id={service_id}&merchant_id={merchant_id}&"
                f"amount={self.transaction_amount}&transaction_param={self.id}&return_url=https://transitgroup.uz"
            )
            payment_url = f'{settings.PROVIDERS["click"]["url"]}/{params}'
        elif self.provider == Provider.UZUM_BANK:
            payment_url = "https://www.apelsin.uz/open-service?serviceId={}&id={}&amount={}".format(
                settings.PROVIDERS[self.provider]["service_id"], self.id, self.transaction_amount
            )

        return payment_url

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class Transaction(BaseModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, verbose_name=_("Order"))
    transaction_id = models.CharField(max_length=255, verbose_name=_("Transaction ID"), null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    status = models.CharField(max_length=63, verbose_name=_("Status"), choices=TransactionStatus.choices)
    paid_at = models.DateTimeField(verbose_name=_("Paid At"), null=True, blank=True)
    cancel_time = models.DateTimeField(verbose_name=_("Cancel Time"), null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.transaction_id}"

    def apply(self):
        self.status = TransactionStatus.PAID
        self.paid_at = timezone.now()
        self.save()
        self.apply_order()

    def apply_order(self):
        self.order.is_paid = True

        self.order.save()

    def cancel(self):
        self.status = TransactionStatus.CANCELED
        self.cancel_time = timezone.now()

        self.save()
        self.order.is_paid = False
        self.order.is_canceled = True
        self.order.save()

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")


class PaymentMerchantRequestLog(BaseModel):
    provider = models.CharField(max_length=63, verbose_name=_("Provider"), choices=Provider.choices)
    header = models.TextField(verbose_name=_("Header"))
    body = models.TextField(verbose_name=_("Body"))
    method = models.CharField(verbose_name=_("Method"), max_length=32)
    response = models.TextField(null=True, blank=True)
    response_status_code = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=32)

    class Meta:
        verbose_name = _("Payment Merchant Request Log")
        verbose_name_plural = _("Payment Merchant Request Logs")
