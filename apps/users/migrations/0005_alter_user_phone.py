# Generated by Django 4.2 on 2023-09-19 17:54

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_full_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=255, region=None, unique=True, verbose_name="Phone number"
            ),
        ),
    ]
