from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.payment.models import (
    Order,
    PaymentMerchantRequestLog,
    Transaction,
    TransactionStatus,
)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "driver", "total_amount", "provider", "is_paid", "is_canceled")
    list_display_links = ("id", "driver")
    list_filter = ("provider", "is_paid", "is_canceled")
    search_fields = (
        "id",
        "driver__user__full_name",
        "driver__user__phone",
        "total_amount",
    )
    # readonly_fields = (
    #     "id",
    #     "user",
    #     "course",
    #     "webinar",
    #     "video_lesson",
    #     "total_amount",
    #     "type",
    #     "payment_type",
    #     "provider",
    #     "is_paid",
    #     "is_canceled",
    # )

    # if you want to create order for testing payment integration you can comment this lines
    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "transaction_id", "amount", "colored_status", "paid_at", "cancel_time")
    list_display_links = ("id", "order")
    list_filter = ("status",)
    search_fields = (
        "id",
        "order__id",
        "transaction_id",
        "amount",
        "paid_at",
        "cancel_time",
        "order__user__full_name",
        "order__user__phone",
    )

    # readonly_fields = ("id", "order", "transaction_id", "amount", "status", "paid_at", "cancel_time")

    def colored_status(self, obj):
        colors = {
            TransactionStatus.WAITING: "gray",
            TransactionStatus.PAID: "green",
            TransactionStatus.FAILED: "red",
            TransactionStatus.CANCELED: "black",
        }
        if obj.status:
            return mark_safe(f'<span style="color:{colors[obj.status]}"><b>{obj.get_status_display()}</b></span>')
        return f"{obj.status} --- null"

    colored_status.short_description = "Status"  # type: ignore

    # if you want to create transaction for testing payment integration you can comment this lines
    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


@admin.register(PaymentMerchantRequestLog)
class PaymentMerchantRequestLogAdmin(admin.ModelAdmin):
    list_display = ["id", "provider", "type", "response_status_code", "created_at"]
    search_fields = ["id", "body", "header", "response", "method"]
    list_filter = ["provider"]
