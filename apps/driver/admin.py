from django.contrib import admin

from apps.driver.models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("id", "driver_full_name", "driver_phone", "car_number")
    list_display_links = (
        "id",
        "driver_full_name",
    )
    search_fields = (
        "id",
        "driver_full_name",
        "driver_phone",
    )

    def driver_full_name(self, obj):
        return obj.user.full_name

    def driver_phone(self, obj):
        return obj.user.phone
