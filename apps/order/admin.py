from django.contrib import admin

from apps.order.models import Location, Order, Request, Trip


admin.site.register(Location)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_full_name",
        "driver_full_name",
        "status",
    )
    list_display_links = ("id", "client_full_name")
    list_filter = ("status",)
    search_fields = (
        "id",
        "client_full_name",
        "driver_full_name",
    )

    def client_full_name(self, obj):
        return obj.order.client.full_name

    def driver_full_name(self, obj):
        return obj.driver.user.full_name


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_full_name",
        "client_phone_number",
        "client_pick_up_address",
        "status",
        "created_at",
    )
    list_display_links = ("id", "client_full_name")
    list_filter = ("status", "type")
    search_fields = (
        "id",
        "client_full_name",
        "client_phone_number",
    )

    def client_full_name(self, obj):
        return obj.client.full_name

    def client_phone_number(self, obj):
        return obj.client.phone

    def client_pick_up_address(self, obj):
        return f"{obj.pick_up_address.city} | {obj.pick_up_address.street}"


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("id", "driver_full_name", "status", "created_at",)
    list_display_links = (
        "id",
        "driver_full_name",
    )
    search_fields = (
        "id",
        "driver_full_name",
        "status",
    )

    def driver_full_name(self, obj):
        return obj.driver.user.full_name
