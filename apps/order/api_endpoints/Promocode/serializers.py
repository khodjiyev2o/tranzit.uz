from rest_framework import serializers
from apps.common.models import Promocode


class PromocodeRetrieveViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promocode
        fields = ("id", "code", "money_amount")
