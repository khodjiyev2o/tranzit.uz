from rest_framework import serializers
from apps.order.models import Order, City


class GeneratePriceSerializer(serializers.ModelSerializer):
    pick_up_city = serializers.CharField(source="pick_up_address.city")
    drop_off_city = serializers.CharField(source="drop_off_address.city")

    class Meta:
        model = Order
        fields = (
            "pick_up_city",
            "drop_off_city",
            "number_of_people",
            "front_right",
            "back_left",
            "back_middle",
            "back_right",
        )

    def validate(self, attrs):
        pick_up_city = attrs.get('pick_up_address')['city']
        drop_off_city = attrs.get('drop_off_address')['city']
        number_of_people = attrs.get("number_of_people")
        front_right = attrs.get("front_right")
        back_left = attrs.get("back_left")
        back_middle = attrs.get("back_middle")
        back_right = attrs.get("back_right")

        # Validate that pick_up_city and drop_off_city are not the same
        if pick_up_city == drop_off_city:
            raise serializers.ValidationError("Pick-up and drop-off cities cannot be the same.")

        # Validate that cities are only "Namangan" or "Tashkent"
        valid_cities = [City.Namangan, City.Tashkent]
        if pick_up_city not in valid_cities or drop_off_city not in valid_cities:
            raise serializers.ValidationError("Cities must be either 'Namangan' or 'Tashkent'.")

        # Validate that the number of people matches the total of boolean fields
        total_seats = sum([front_right, back_left, back_middle, back_right])
        if number_of_people != total_seats:
            raise serializers.ValidationError("Number of people must match the total of seat selections.")

        return attrs
