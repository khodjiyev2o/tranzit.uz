import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status

from helpers.cache import CacheTypes, generate_cache_key


@pytest.mark.django_db
def test_send_sms_for_login_driver(client, new_driver):
    url = reverse("driver-login-send-sms")
    payload = {
        "phone": f"{new_driver.user.phone}",
    }
    response = client.post(url, data=payload, content_type="application/json")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert list(response.json().keys()) == ["session"]


@pytest.mark.django_db
def test_send_sms_for_driver_to_login_no_existing_phone(client):
    url = reverse("driver-login-send-sms")
    payload = {
        "phone": "+9982229900",
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 400
    assert response.json()["errors"][0]["code"] == "phone_invalid_phone_number"
    assert response.json()["errors"][0]["message"] == "The phone number entered is not valid."


@pytest.mark.django_db
def test_send_sms_for_driver_not_found(client):
    url = reverse("driver-login-send-sms")
    payload = {
        "phone": "+998887716677",
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 400
    assert response.json()["errors"][0]["code"] == "driver_not_found"
    assert response.json()["errors"][0]["message"] == "Driver not found!"


@pytest.mark.django_db
def test_send_sms_for_driver_timeout_error(client, new_driver):
    url = reverse("driver-login-send-sms")
    payload = {
        "phone": str(new_driver.user.phone),
    }
    cache_type = CacheTypes.registration_sms_verification
    phone = payload["phone"]
    session = "Sdadasdada"
    code = 123456
    cache.set(generate_cache_key(cache_type, phone, session), code, timeout=5)
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 400
    assert response.json()["errors"][0]["code"] == "phone_timeout"
