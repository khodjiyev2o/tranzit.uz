from rest_framework import serializers

from apps.driver.models import Driver


class CreateDriverAccountSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Driver
        fields = (
            "city",
            "tex_passport",
            "driving_license",
            "car_model",
            "car_number",
            "car_category",
            "has_air_conditioner",
            "has_baggage",
            "smoking_allowed",
            "status",
        )
