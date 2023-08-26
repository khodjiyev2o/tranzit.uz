from apps.common.models import Promocode, UserPromocode
from django.contrib import admin


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "money_amount", "max_usage_count", "expires_at")
    list_display_links = ("id", "code")
    list_filter = ("code",)
    search_fields = ("code", "money_amount")


@admin.register(UserPromocode)
class UserPromocodeAdmin(admin.ModelAdmin):
    list_display = ("id", "promocode", "user", "created_at")
    list_display_links = ("id", "user")
    list_filter = ("promocode",)
    search_fields = ("promocode", "user")
