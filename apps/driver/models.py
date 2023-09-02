from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.users.models import User


class City(models.TextChoices):
    Namangan = "Namangan", _("Namangan")
    Tashkent = "Tashkent", _("Tashkent")
    Toshkent = "Toshkent", _("Toshkent")
    Toshkent_shahar = "Toshkent shahar", _("Toshkent shahar")
    Namangan_Viloyati = "Namangan Viloyati", _("Namangan Viloyati")


class CarModel(models.TextChoices):
    GENTRA = "Gentra", _("Gentra")
    LACETTI = "Lacetti", _("Lacetti")
    COBALT = "Cobalt", _("Cobalt")
    NEXIA_2 = "Nexia_2", _("Nexia 2")
    NEXIA_3 = "Nexia 3", _("Nexia 3")
    SPARK = "Spark", _("Spark")
    EPICA = "Epica", _("Epica")
    CAPTIVA = "Captiva", _("Captiva")
    TRACKER = "Tracker", _("Tracker")
    TRACKER_2 = "Tracker 2", _("Tracker 2")
    MALIBU = "Malibu", _("Malibu")
    MALIBU_2 = "Malibu 2", _("Malibu 2")
    EQUINOX = "Equinox", _("Equinox")


class CarCategory(models.TextChoices):
    COMFORT = "Comfort", _("Comfort")
    BUSINESS = "Business", _("Business")


class DriverStatus(models.TextChoices):
    IN_MODERATION = "In_Moderation", _("In Moderation")
    ACTIVE = "Active", _("Active")
    BLOCKED = "Blocked", _("Blocked")


class Driver(BaseModel):
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="driver")
    # register info
    city = models.CharField(max_length=256, choices=City.choices, default=City.Namangan, verbose_name=_("City"))
    tex_passport = models.CharField(max_length=10, verbose_name=_("Tex Passport"))
    driving_license = models.CharField(max_length=9, verbose_name=_("Driving License"))
    car_model = models.CharField(max_length=256, verbose_name=_("Car Model"))
    car_number = models.CharField(max_length=8, verbose_name=_("Car Number"), unique=True)
    car_category = models.CharField(max_length=256, verbose_name=_("Car Category"), choices=CarCategory.choices)
    has_air_conditioner = models.BooleanField(default=True, verbose_name=_("Has Air Conditioner"))
    has_baggage = models.BooleanField(default=True, verbose_name=_("Has Baggage"))
    smoking_allowed = models.BooleanField(default=False, verbose_name=_("Smoking Allowed"))
    # driver status
    status = models.CharField(
        max_length=256,
        verbose_name=_("Driver Status"),
        choices=DriverStatus.choices,
        default=DriverStatus.IN_MODERATION,
    )
    is_online = models.BooleanField(verbose_name=_("Is Online"), default=False)
    balance = models.IntegerField(
        verbose_name=_("Driver Balance"),
        default=100000,
    )

    def __str__(self):
        return f"Driver| {self.user.full_name} - {self.balance}"

    class Meta:
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")
