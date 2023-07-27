# Generated by Django 4.2 on 2023-07-26 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="city",
            field=models.CharField(
                choices=[("Namangan", "Namangan"), ("Tashkent", "Tashkent")],
                default="Namangan",
                max_length=256,
                verbose_name="City",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="delivery_user_phone",
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name="Phone number"),
        ),
    ]