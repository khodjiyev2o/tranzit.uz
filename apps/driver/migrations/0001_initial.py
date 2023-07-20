# Generated by Django 4.2 on 2023-07-20 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Driver",
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
                (
                    "tex_passport",
                    models.CharField(max_length=10, verbose_name="Tex Passport"),
                ),
                (
                    "driving_license",
                    models.CharField(max_length=9, verbose_name="Driving License"),
                ),
                (
                    "car_model",
                    models.CharField(
                        choices=[
                            ("Gentra", "Gentra"),
                            ("Lacetti", "Lacetti"),
                            ("Cobalt", "Cobalt"),
                            ("Nexia_2", "Nexia 2"),
                            ("Nexia 3", "Nexia 3"),
                            ("Spark", "Spark"),
                            ("Epica", "Epica"),
                            ("Captiva", "Captiva"),
                            ("Tracker", "Tracker"),
                            ("Tracker 2", "Tracker 2"),
                            ("Malibu", "Malibu"),
                            ("Malibu 2", "Malibu 2"),
                            ("Equinox", "Equinox"),
                        ],
                        max_length=256,
                        verbose_name="Car Model",
                    ),
                ),
                (
                    "car_number",
                    models.CharField(max_length=8, verbose_name="Car Number"),
                ),
                (
                    "car_category",
                    models.CharField(
                        choices=[("Comfort", "Comfort"), ("Business", "Business")],
                        max_length=256,
                        verbose_name="Car Category",
                    ),
                ),
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
                    "status",
                    models.CharField(
                        choices=[
                            ("In Moderation", "In Moderation"),
                            ("Active", "Active"),
                            ("Blocked", "Blocked"),
                        ],
                        default="In Moderation",
                        max_length=256,
                        verbose_name="Driver Status",
                    ),
                ),
                (
                    "is_online",
                    models.BooleanField(default=False, verbose_name="Is Online"),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=100000,
                        max_digits=10,
                        verbose_name="Driver Balance",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Driver",
                "verbose_name_plural": "Drivers",
            },
        ),
    ]
