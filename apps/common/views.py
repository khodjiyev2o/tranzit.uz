from django.http import JsonResponse
from rest_framework.views import APIView

from apps.driver.models import CarModel, City


class CarModelListView(APIView):
    def get(self, request):
        cars = list(CarModel)
        return JsonResponse({"cars": cars})


class CitiesListView(APIView):
    def get(self, request):
        cities = list(City)
        return JsonResponse({"cities": cities})


__all__ = ["CitiesListView", "CarModelListView"]
