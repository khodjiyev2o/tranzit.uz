# Generated by Django 4.2 on 2023-07-26 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_alter_order_promocode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="comment",
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name="Comment"),
        ),
    ]
