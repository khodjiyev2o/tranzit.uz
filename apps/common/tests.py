import pytest
from django.urls import reverse

from apps.driver.models import CarModel, City


@pytest.mark.django_db
def test_cities_list(client):
    url = reverse("city-list")
    response = client.get(url)
    cities = list(City)
    assert response.status_code == 200
    assert response.json() == {"cities": cities}


@pytest.mark.django_db
def test_cars_list(client):
    url = reverse("car-list")
    response = client.get(url)
    cars = list(CarModel)
    assert response.status_code == 200
    assert response.json() == {"cars": cars}
