from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "is_staff")
    list_display_links = ("id", "full_name")
    list_filter = ("is_staff", "created_at")
    search_fields = (
        "id",
        "full_name",
        "phone",
    )
