# Generated by Django 4.2 on 2023-07-26 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("driver", "0002_alter_driver_car_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="city",
            field=models.CharField(
                choices=[("Namangan", "Namangan"), ("Tashkent", "Tashkent")],
                default="Namangan",
                max_length=256,
                verbose_name="City",
            ),
        ),
    ]
