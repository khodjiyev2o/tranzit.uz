import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status

from helpers.cache import CacheTypes, generate_cache_key


@pytest.mark.django_db
def test_driver_send_sms_and_verify(client):
    # send sms first
    url = reverse("driver-register-send-sms")
    payload = {
        "phone": "+998913582680",
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    code = cache.get(
        generate_cache_key(CacheTypes.registration_sms_verification, "+998913582680", response.json()["session"])
    )

    # verify phone via sms
    url = reverse("driver-register-verify-phone")
    data = {"code": code, "session": response.json()["session"], "phone": "+998913582680", "full_name": "Samandar"}
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    assert list(response.json().keys()) == ["access", "refresh"]


@pytest.mark.django_db
def test_driver_send_sms_wrong_code(client):
    # send sms first
    url = reverse("driver-register-send-sms")
    payload = {
        "phone": "+998996613344",
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK

    # verify phone via sms
    url = reverse("driver-register-verify-phone")
    data = {"code": 123456, "session": response.json()["session"], "phone": "+998996613344", "full_name": "Samandar"}
    response = client.post(url, data=data, content_type="application/json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['errors'][0]['code'] == 'code_invalid'
