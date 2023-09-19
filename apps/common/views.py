from apps.driver.models import CarModel, City
from apps.common.models import FrontTranslation
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError


class CarModelListView(APIView):
    def get(self, request):
        cars = list(CarModel)
        return Response({"cars": cars})


class CitiesListView(APIView):
    def get(self, request):
        cities = list(City)
        return Response({"cities": cities})


class FrontTranslationListAPIView(APIView):

    @swagger_auto_schema(manual_parameters=[openapi.Parameter("lang", openapi.IN_QUERY, type="string")])
    def get(self, request):
        lang = request.query_params.get("lang", None)
        if lang is None:
            raise ValidationError(detail={"language": _("lang is required.")}, code="required")

        if lang not in ["uz", "ru", "en"]:
            raise ValidationError(detail={"language": _("lang must be in correct format.(uz,en,ru)")},
                                  code="invalid")

        data = FrontTranslation.objects.all().values(
            "key",
            f"text_{lang}",
        )
        dict_data = {}

        for d in data:
            dict_data[d["key"]] = d[f"text_{lang}"]

        return Response(dict_data)


__all__ = ["CitiesListView", "CarModelListView", 'FrontTranslationListAPIView']
