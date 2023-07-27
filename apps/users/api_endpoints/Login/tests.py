import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status

from helpers.cache import CacheTypes, generate_cache_key
from tests.factories import UserFactory


@pytest.mark.django_db
def test_user_send_sms_login(client):
    new_user = UserFactory(phone="+998912249735")
    url = reverse("user-login-send-sms")
    payload = {
        "phone": new_user.phone,
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK

    assert list(response.json().keys()) == ["session"]


@pytest.mark.django_db
def test_user_send_sms_login_timeout_error(client, new_user):
    payload = {
        "phone": str(new_user.phone),
    }
    cache_type = CacheTypes.registration_sms_verification
    phone = payload["phone"]
    session = "Sdadasdada"
    code = 123456
    cache.set(generate_cache_key(cache_type, phone, session), code, timeout=5)

    url = reverse("user-login-send-sms")
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 400
    assert response.json()["phone"] == "SMS is already sent!"


@pytest.mark.django_db
def test_send_sms_user_login_with_existing_phone(client):
    url = reverse("user-login-send-sms")
    payload = {
        "phone": "+998913665113",
    }
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 404
    assert response.json()["success"] is False
    assert response.json()["message"] == "User not found!"
