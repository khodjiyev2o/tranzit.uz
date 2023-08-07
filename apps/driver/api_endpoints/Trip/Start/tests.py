import pytest
from django.urls import reverse

from apps.order.models import Trip
from tests.factories import TripFactory


@pytest.mark.django_db
def test_driver_start_trip(client, new_driver, new_order):
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."

    url = reverse("driver-trip-start")
    response = client.patch(url, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully started the trip"


@pytest.mark.django_db
def test_driver_start_trip_not_found_at_all(client, new_driver, new_order):
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}

    url = reverse("driver-trip-start")
    response = client.patch(url, **headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Not found."


@pytest.mark.django_db
def test_driver_start_trip_not_found_active_trip(client, new_driver, new_order):
    TripFactory(driver=new_driver, status=Trip.TripStatus.IN_PROCESS)
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}

    url = reverse("driver-trip-start")
    response = client.patch(url, **headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Not found."
