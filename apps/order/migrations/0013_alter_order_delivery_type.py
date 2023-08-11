# Generated by Django 4.2 on 2023-08-08 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0012_alter_order_delivery_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="delivery_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("document", "document"),
                    ("money", "money"),
                    ("box", "box"),
                    ("dishes", "dishes"),
                    ("secret", "secret"),
                ],
                max_length=256,
                null=True,
                verbose_name="Delivery Type",
            ),
        ),
    ]