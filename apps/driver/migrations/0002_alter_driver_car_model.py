# Generated by Django 4.2 on 2023-07-24 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("driver", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="car_model",
            field=models.CharField(max_length=256, verbose_name="Car Model"),
        ),
    ]
