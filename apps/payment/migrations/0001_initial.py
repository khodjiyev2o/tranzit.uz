# Generated by Django 4.2 on 2023-09-02 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("driver", "0007_alter_driver_city"),
    ]

    operations = [
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
                    "provider",
                    models.CharField(
                        choices=[
                            ("payme", "Payme"),
                            ("click", "Click"),
                            ("karmon_pay", "Karmon Pay"),
                            ("uzum_bank", "Uzum Bank"),
                            ("card", "Card"),
                        ],
                        max_length=63,
                        verbose_name="Provider",
                    ),
                ),
                (
                    "total_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Total Amount"
                    ),
                ),
                ("is_paid", models.BooleanField(default=False, verbose_name="Is Paid")),
                (
                    "is_canceled",
                    models.BooleanField(default=False, verbose_name="Is Canceled"),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="driver.driver",
                        verbose_name="Driver",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        ),
        migrations.CreateModel(
            name="PaymentMerchantRequestLog",
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
                    "provider",
                    models.CharField(
                        choices=[
                            ("payme", "Payme"),
                            ("click", "Click"),
                            ("karmon_pay", "Karmon Pay"),
                            ("uzum_bank", "Uzum Bank"),
                            ("card", "Card"),
                        ],
                        max_length=63,
                        verbose_name="Provider",
                    ),
                ),
                ("header", models.TextField(verbose_name="Header")),
                ("body", models.TextField(verbose_name="Body")),
                ("method", models.CharField(max_length=32, verbose_name="Method")),
                ("response", models.TextField(blank=True, null=True)),
                ("response_status_code", models.IntegerField(blank=True, null=True)),
                ("type", models.CharField(max_length=32)),
            ],
            options={
                "verbose_name": "Payment Merchant Request Log",
                "verbose_name_plural": "Payment Merchant Request Logs",
            },
        ),
        migrations.CreateModel(
            name="Transaction",
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
                    "transaction_id",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Transaction ID"
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Amount"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("waiting", "Waiting"),
                            ("paid", "Paid"),
                            ("failed", "Failed"),
                            ("canceled", "Canceled"),
                        ],
                        max_length=63,
                        verbose_name="Status",
                    ),
                ),
                (
                    "paid_at",
                    models.DateTimeField(blank=True, null=True, verbose_name="Paid At"),
                ),
                (
                    "cancel_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Cancel Time"
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payment.order",
                        verbose_name="Order",
                    ),
                ),
            ],
            options={
                "verbose_name": "Transaction",
                "verbose_name_plural": "Transactions",
            },
        ),
    ]
