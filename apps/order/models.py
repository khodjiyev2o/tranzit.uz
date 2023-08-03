from django.core.exceptions import ValidationError
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
    number_of_people = models.IntegerField(default=1, verbose_name=_("Number Of People"))
    front_right = models.BooleanField(default=False, verbose_name=_("FRONT RIGHT"))
    back_left = models.BooleanField(default=False, verbose_name=_("BACK LEFT"))
    back_middle = models.BooleanField(default=False, verbose_name=_("BACK MIDDLE"))
    back_right = models.BooleanField(default=False, verbose_name=_("BACK RIGHT"))
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

    def clean(self):
        """To control the number of people and seats that they occupy"""
        if self.type == Order.OrderType.PERSON:
            number_of_seats = sum([self.front_right, self.back_left, self.back_middle, self.back_right])
            if number_of_seats != self.number_of_people:
                raise ValidationError(
                    _(f"For {self.number_of_people} person, {self.number_of_people} seats must be selected.")
                )
        else:
            if not self.delivery_user_phone:
                raise ValidationError(_("Phone number is required for delivery orders."))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class Trip(BaseModel):
    class TripStatus(models.TextChoices):
        ACTIVE = "ACTIVE", _("ACTIVE")
        IN_PROCESS = "IN_PROCESS", _("IN_PROCESS")
        COMPLETED = "COMPLETED", _("COMPLETED")

    driver = models.ForeignKey(Driver, verbose_name=_("Driver"), on_delete=models.CASCADE)
    client = models.ManyToManyField(
        Order,
        verbose_name=_("Person Orders"),
        related_name="person_orders",
        blank=True,
        limit_choices_to={"type__in": [Order.OrderType.PERSON]},
    )
    delivery = models.ManyToManyField(
        Order,
        verbose_name=_("Delivery"),
        related_name="deliveries",
        blank=True,
        limit_choices_to={"type__in": [Order.OrderType.DELIVERY]},
    )
    status = models.CharField(
        max_length=256, choices=TripStatus.choices, default=TripStatus.ACTIVE, verbose_name=_("Status")
    )

    def __str__(self):
        return f"{self.driver.user.full_name} | {self.status}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Trip, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Trip")
        verbose_name_plural = _("Trips")


class Request(BaseModel):
    class RequestStatus(models.TextChoices):
        WAITING = "Waiting", _("Waiting")
        ACCEPTED = "Accepted", _("Accepted")
        CANCELED = "Canceled", _("Canceled")

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Order"))
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, verbose_name=_("Driver"))
    status = models.CharField(max_length=256, choices=RequestStatus.choices, default=RequestStatus.WAITING)

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")
