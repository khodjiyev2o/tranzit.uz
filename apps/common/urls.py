from django.urls import path

from apps.common.views import CarModelListView, CitiesListView, FrontTranslationListAPIView


urlpatterns = [
    path("cars/", CarModelListView.as_view(), name="car-list"),
    path("cities/", CitiesListView.as_view(), name="city-list"),
    path("FrontTranslationList/", FrontTranslationListAPIView.as_view(), name="front_translation"),
]
