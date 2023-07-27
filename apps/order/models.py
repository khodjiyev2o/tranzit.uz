from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.driver.models import CarCategory, City, Driver
from apps.users.models import User


class Location(BaseModel):
    city = models.CharField(max_length=256, choices=City.choices, default=City.Namangan, verbose_name=_("City"))
    street = models.CharField(max_length=256, verbose_name=_("Street"))
    latitude = models.CharField(max_length=256, verbose_name=_("Latitude"))
    longitude = models.CharField(max_length=256, verbose_name=_("Longitude"))

    def __str__(self):
        return f"{self.city} | {self.street}"

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        WAITING = "Waiting", _("Waiting")
        REQUESTED = "Requested", _("Requested")
        IN_PROGRESS = "In_Progress", _("In_Progress")
        COMPLETED = "Completed", _("Completed")
        CANCELED = "Canceled", _("Canceled")

    class Seat(models.TextChoices):
        FRONT_RIGHT = "front_right", _("FRONT RIGHT")
        BACK_LEFT = "back_left", _("BACK LEFT")
        BACK_MIDDLE = "back_middle", _("BACK MIDDLE")
        BACK_RIGHT = "back_right", _("BACK RIGHT")

    class OrderType(models.TextChoices):
        PERSON = "PERSON", _("PERSON")
        DELIVERY = "DELIVERY", _("DELIVERY")

    pick_up_address = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="pickup_address"
    )
    drop_off_address = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="dropoff_address"
    )
    status = models.CharField(
        max_length=256, choices=OrderStatus.choices, default=OrderStatus.REQUESTED, verbose_name=_("Status")
    )
    car_category = models.CharField(
        max_length=256, verbose_name=_("Car Category"), choices=CarCategory.choices, default=CarCategory.COMFORT
    )
    price = models.IntegerField(verbose_name=_("Order Price"), default=120000)
    seat = models.CharField(max_length=256, choices=Seat.choices, verbose_name=_("Seat Choices"))
    type = models.CharField(
        max_length=256, verbose_name=_("Order Type"), choices=OrderType.choices, default=OrderType.PERSON
    )
    delivery_user_phone = models.CharField(_("Phone number"), max_length=13, null=True, blank=True)
    approximate_leave_time = models.DateTimeField(verbose_name=_("Approximate Leave Time "))
    comment = models.CharField(max_length=256, verbose_name=_("Comment"), null=True, blank=True)
    has_air_conditioner = models.BooleanField(default=True, verbose_name=_("Has Air Conditioner"))
    has_baggage = models.BooleanField(default=True, verbose_name=_("Has Baggage"))
    smoking_allowed = models.BooleanField(default=False, verbose_name=_("Smoking Allowed"))
    promocode = models.CharField(max_length=15, verbose_name=_("Promocode"), null=True, blank=True)

    # FK
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Client"))

    def __str__(self):
        return f"{self.client.full_name} | {self.pick_up_address.street}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class Trip(BaseModel):
    class TripStatus(models.TextChoices):
        ACTIVE = "ACTIVE", _("ACTIVE")
        COMPLETED = "COMPLETED", _("COMPLETED")

    driver = models.ForeignKey(Driver, verbose_name=_("Driver"), on_delete=models.CASCADE)
    front_right_seat = models.ForeignKey(
        Order, models.SET_NULL, verbose_name=_("FRONT RIGHT"), related_name="front_trip", null=True, blank=True
    )
    back_left_seat = models.ForeignKey(
        Order, models.SET_NULL, related_name="back_left_trip", verbose_name=_("BACK LEFT"), null=True, blank=True
    )
    back_middle_seat = models.ForeignKey(
        Order, models.SET_NULL, related_name="back_middle_trip", verbose_name=_("BACK MIDDLE"), null=True, blank=True
    )
    back_right_seat = models.ForeignKey(
        Order, models.SET_NULL, related_name="back_right_trip", verbose_name=_("BACK RIGHT"), null=True, blank=True
    )
    delivery = models.ManyToManyField(Order, verbose_name=_("Delivery"), related_name="questions")
    status = models.CharField(
        max_length=256, choices=TripStatus.choices, default=TripStatus.ACTIVE, verbose_name=_("Status")
    )

    def __str__(self):
        return f"{self.driver.user.full_name} | {self.status}"

    class Meta:
        verbose_name = _("Trip")
        verbose_name_plural = _("Trips")


class Request(BaseModel):
    class RequestStatus(models.TextChoices):
        WAITING = "Waiting", _("Waiting")
        ACCEPTED = "Accepted", _("Accepted")
        CANCELED = "Canceled", _("Canceled")

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Order"))
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name=_("Driver"))
    status = models.CharField(max_length=256, choices=RequestStatus.choices, default=RequestStatus.WAITING)


    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")
