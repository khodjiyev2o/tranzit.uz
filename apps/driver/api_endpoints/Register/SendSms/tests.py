import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_driver_send_sms_for_register(client):
    url = reverse("driver-register-send-sms")
    payload = {
        "phone": "+998913665113",
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    assert list(response.json().keys()) == ["session"]


@pytest.mark.django_db
def test_driver_send_sms_for_register_driver_exists(client, new_driver):
    url = reverse("driver-register-send-sms")
    payload = {
        "phone": new_driver.user.phone,
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 409
    assert response.json()["success"] is False
    assert response.json()["message"] == "Driver account already exists!"
