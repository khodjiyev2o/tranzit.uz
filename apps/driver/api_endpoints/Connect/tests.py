import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_driver_online_mode(client, new_driver):
    url = reverse("driver-online-status")

    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    response = client.put(url, content_type="application/json", **headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert response.json()["is_online"] is True


@pytest.mark.django_db
def test_driver_offline_mode(client, new_driver):
    url = reverse("driver-offline-status")

    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    response = client.put(url, content_type="application/json", **headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert response.json()["is_online"] is False
