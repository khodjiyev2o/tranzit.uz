import pytest
from django.urls import reverse

from apps.driver.models import DriverStatus
from tests.factories import DriverFactory


@pytest.mark.django_db
def test_get_driver_status(client, new_driver):
    url = reverse("driver-status")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    response = client.get(url, **headers)
    assert response.status_code == 200
    assert response.json()["status"] == str(new_driver.status)


@pytest.mark.django_db
def test_get_driver_status_in_moderation(client):
    new_driver = DriverFactory(status=DriverStatus.IN_MODERATION)
    url = reverse("driver-status")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    response = client.get(url, **headers)
    assert response.status_code == 200
    assert response.json()["status"] == str(DriverStatus.IN_MODERATION)
