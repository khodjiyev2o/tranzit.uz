from rest_framework import serializers

from .utils import PaymeMethods


class PaymeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    method = serializers.ChoiceField(choices=PaymeMethods.choices())
    params = serializers.JSONField()
