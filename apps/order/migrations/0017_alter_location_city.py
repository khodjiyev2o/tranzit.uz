# Generated by Django 4.2 on 2023-09-02 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0016_alter_location_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="city",
            field=models.CharField(
                blank=True,
                default="Namangan",
                max_length=256,
                null=True,
                verbose_name="City",
            ),
        ),
    ]
