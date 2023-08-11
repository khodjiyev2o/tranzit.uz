from rest_framework import serializers

from apps.driver.models import Driver
from apps.order.api_endpoints.List.serializers import LocationSerializer
from apps.order.models import Order, Trip


class DriverSerializerForTrip(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("has_air_conditioner", "has_baggage", "smoking_allowed")


class DriverTripClientSerializer(serializers.ModelSerializer):
    seats = serializers.SerializerMethodField()
    client_full_name = serializers.CharField(source="client.full_name")
    client_phone_number = serializers.CharField(source="client.phone")
    pick_up_address = LocationSerializer()
    drop_off_address = LocationSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "client_full_name",
            "client_phone_number",
            "price",
            "approximate_leave_time",
            "seats",
            "pick_up_address",
            "drop_off_address",
        )

    def get_seats(self, obj):
        chosen_seats = []
        if obj.front_right is True:
            chosen_seats.append("front_right")
        if obj.back_left is True:
            chosen_seats.append("back_left")
        if obj.back_middle is True:
            chosen_seats.append("back_middle")
        if obj.back_right is True:
            chosen_seats.append("back_right")
        return chosen_seats


class DriverTripDeliverySerializer(serializers.ModelSerializer):
    pick_up_address = LocationSerializer()
    drop_off_address = LocationSerializer()
    client_phone_number = serializers.CharField(source="client.phone")

    class Meta:
        model = Order
        fields = (
            "id",
            "client_phone_number",
            "delivery_user_phone",
            "delivery_type",
            "price",
            "approximate_leave_time",
            "pick_up_address",
            "drop_off_address",
        )


class DriverTripSerializer(serializers.ModelSerializer):
    driver = DriverSerializerForTrip()
    client = DriverTripClientSerializer(many=True)
    delivery = DriverTripDeliverySerializer(many=True)
    pick_up_address = serializers.SerializerMethodField()
    drop_off_address = serializers.SerializerMethodField()
    approximate_leave_time = serializers.SerializerMethodField()
    seats = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = (
            "id",
            "status",
            "pick_up_address",
            "drop_off_address",
            "approximate_leave_time",
            "driver",
            "seats",
            "client",
            "delivery",
        )

    def get_seats(self, obj):
        seats = {
            "front_right": False,
            "back_left": False,
            "back_middle": False,
            "back_right": False,
        }
        if obj.client.exists():
            for client_order in obj.client.all():
                if client_order.front_right:
                    seats["front_right"] = True
                if client_order.back_left:
                    seats["back_left"] = True
                if client_order.back_middle:
                    seats["back_middle"] = True
                if client_order.back_right:
                    seats["back_right"] = True
        return seats

    def get_approximate_leave_time(self, obj):
        # Check if there is any data in the client field
        approximate_leave_time = None

        if obj.client.exists():
            for client in obj.client.all():
                if approximate_leave_time is None:
                    approximate_leave_time = client.approximate_leave_time
                elif approximate_leave_time < client.approximate_leave_time:
                    approximate_leave_time = client.approximate_leave_time

        #  check the delivery field
        if obj.delivery.exists():
            for delivery in obj.delivery.all():
                if approximate_leave_time is None:
                    approximate_leave_time = delivery.approximate_leave_time

                elif approximate_leave_time < delivery.approximate_leave_time:
                    approximate_leave_time = delivery.approximate_leave_time

        return approximate_leave_time

    def get_pick_up_address(self, obj):
        # Check if there is any data in the client field
        if obj.client.exists():
            client_order = obj.client.first()
            return client_order.pick_up_address.city

        # If client field is empty, check the delivery field
        elif obj.delivery.exists():
            delivery_order = obj.delivery.first()
            return delivery_order.pick_up_address.city

        # If both client and delivery fields are empty, return None
        else:
            return None

    def get_drop_off_address(self, obj):
        # Check if there is any data in the client field
        if obj.client.exists():
            client_order = obj.client.first()
            return client_order.drop_off_address.city

        # If client field is empty, check the delivery field
        elif obj.delivery.exists():
            delivery_order = obj.delivery.first()
            return delivery_order.drop_off_address.city

        # If both client and delivery fields are empty, return None
        else:
            return None
