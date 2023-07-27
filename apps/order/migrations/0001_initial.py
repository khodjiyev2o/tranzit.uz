# Generated by Django 4.2 on 2023-07-24 04:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("driver", "0002_alter_driver_car_model"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "city",
                    models.CharField(
                        choices=[("Namangan", "Namangan")],
                        default="Namangan",
                        max_length=256,
                        verbose_name="City",
                    ),
                ),
                ("street", models.CharField(max_length=256, verbose_name="Street")),
                ("latitude", models.CharField(max_length=256, verbose_name="Latitude")),
                (
                    "longitude",
                    models.CharField(max_length=256, verbose_name="Longitude"),
                ),
            ],
            options={
                "verbose_name": "Location",
                "verbose_name_plural": "Locations",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("REQUESTED", "REQUESTED"),
                            ("IN_PROGRESS", "IN_PROGRESS"),
                            ("COMPLETED", "COMPLETED"),
                            ("CANCELED", "CANCELED"),
                        ],
                        default="REQUESTED",
                        max_length=256,
                        verbose_name="Status",
                    ),
                ),
                (
                    "car_category",
                    models.CharField(
                        choices=[("Comfort", "Comfort"), ("Business", "Business")],
                        default="Comfort",
                        max_length=256,
                        verbose_name="Car Category",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=120000,
                        max_digits=10,
                        verbose_name="Order Price",
                    ),
                ),
                (
                    "seat",
                    models.CharField(
                        choices=[
                            ("FRONT_RIGHT", "FRONT RIGHT"),
                            ("BACK_LEFT", "BACK LEFT"),
                            ("BACK_MIDDLE", "BACK MIDDLE"),
                            ("BACK_RIGHT", "BACK RIGHT"),
                        ],
                        max_length=256,
                        verbose_name="Seat Choices",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("PERSON", "PERSON"), ("DELIVERY", "DELIVERY")],
                        default="PERSON",
                        max_length=256,
                        verbose_name="Order Type",
                    ),
                ),
                (
                    "delivery_user_phone",
                    models.CharField(max_length=13, verbose_name="Phone number"),
                ),
                (
                    "approximate_leave_time",
                    models.DateTimeField(verbose_name="Approximate Leave Time "),
                ),
                ("comment", models.CharField(max_length=256, verbose_name="Comment")),
                (
                    "has_air_conditioner",
                    models.BooleanField(default=True, verbose_name="Has Air Conditioner"),
                ),
                (
                    "has_baggage",
                    models.BooleanField(default=True, verbose_name="Has Baggage"),
                ),
                (
                    "smoking_allowed",
                    models.BooleanField(default=False, verbose_name="Smoking Allowed"),
                ),
                (
                    "promocode",
                    models.CharField(max_length=15, verbose_name="Promocode"),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Client",
                    ),
                ),
                (
                    "drop_off_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="dropoff_address",
                        to="order.location",
                    ),
                ),
                (
                    "pick_up_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="pickup_address",
                        to="order.location",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        ),
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("ACTIVE", "ACTIVE"), ("COMPLETED", "COMPLETED")],
                        default="ACTIVE",
                        max_length=256,
                        verbose_name="Status",
                    ),
                ),
                (
                    "back_left_seat",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="back_left_trip",
                        to="order.order",
                        verbose_name="BACK LEFT",
                    ),
                ),
                (
                    "back_middle_seat",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="back_middle_trip",
                        to="order.order",
                        verbose_name="BACK MIDDLE",
                    ),
                ),
                (
                    "back_right_seat",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="back_right_trip",
                        to="order.order",
                        verbose_name="BACK RIGHT",
                    ),
                ),
                (
                    "delivery",
                    models.ManyToManyField(
                        related_name="questions",
                        to="order.order",
                        verbose_name="Delivery",
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="driver.driver",
                        verbose_name="Driver",
                    ),
                ),
                (
                    "front_right_seat",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="front_trip",
                        to="order.order",
                        verbose_name="FRONT RIGHT",
                    ),
                ),
            ],
            options={
                "verbose_name": "Trip",
                "verbose_name_plural": "Trips",
            },
        ),
    ]
