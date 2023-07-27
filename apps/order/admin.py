from django.contrib import admin

from apps.order.models import Location, Order, Trip, Request


admin.site.register(Location)
admin.site.register(Trip)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_full_name",
        "driver_full_name",
        "status",
    )
    list_display_links = ("id", "client_full_name")
    list_filter = ("status", )
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
        "client_drop_off_address",
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

    def client_drop_off_address(self, obj):
        return f"{obj.drop_off_address.city} | {obj.drop_off_address.street}"
