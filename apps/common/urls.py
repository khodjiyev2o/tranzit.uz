from django.urls import path

from apps.common.views import CarModelListView, CitiesListView


urlpatterns = [
    path("cars/", CarModelListView.as_view(), name="car-list"),
    path("cities/", CitiesListView.as_view(), name="city-list"),
]
