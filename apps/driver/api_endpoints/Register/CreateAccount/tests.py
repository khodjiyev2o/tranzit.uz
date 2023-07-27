import pytest
from django.urls import reverse
from rest_framework import status

from apps.driver.models import CarCategory, CarModel, City, DriverStatus


@pytest.mark.django_db
def test_driver_create_account(client, new_user):
    url = reverse("driver-create-account")
    payload = {
        "city": City.Namangan,
        "tex_passport": "ABC1234567",
        "driving_license": "AB1234567",
        "car_model": CarModel.GENTRA,
        "car_number": "01717CEA",
        "car_category": CarCategory.COMFORT,
        "has_air_conditioner": True,
        "has_baggage": True,
        "smoking_allowed": False,
    }
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_user.tokens.get('access')}"}
    response = client.post(url, data=payload, content_type="application/json", **headers)
    assert response.status_code == status.HTTP_201_CREATED

    assert response.json()["city"] == payload["city"]
    assert response.json()["tex_passport"] == payload["tex_passport"]
    assert response.json()["driving_license"] == payload["driving_license"]
    assert response.json()["car_model"] == payload["car_model"]
    assert response.json()["car_number"] == payload["car_number"]
    assert response.json()["car_category"] == payload["car_category"]
    assert response.json()["has_air_conditioner"] == payload["has_air_conditioner"]
    assert response.json()["has_baggage"] == payload["has_baggage"]
    assert response.json()["smoking_allowed"] == payload["smoking_allowed"]
    assert response.json()["status"] == DriverStatus.IN_MODERATION
