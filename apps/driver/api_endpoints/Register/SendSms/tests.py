import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_driver_send_sms_for_register(client):
    url = reverse("driver-register-send-sms")
    payload = {
        "phone": "+998692249735",
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    assert list(response.json().keys()) == ["session"]


@pytest.mark.django_db
def test_driver_send_sms_for_register_timeout_error(client):
    url = reverse("driver-register-send-sms")
    payload = {
        "phone": "+998692249735",
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["errors"][0]["code"] == "phone_timeout"


@pytest.mark.django_db
def test_driver_send_sms_for_register_driver_exists(client, new_driver):
    url = reverse("driver-register-send-sms")
    payload = {
        "phone": f"{new_driver.user.phone}",
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 400
    assert response.json()["errors"][0]["code"] == "driver_already_exists"
