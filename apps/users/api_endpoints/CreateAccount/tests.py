import pytest
from django.core.cache import cache
from django.urls import reverse

from helpers.cache import CacheTypes, generate_cache_key


@pytest.mark.django_db
def test_create_user_profile(client):

    payload = {"phone": "+998913665113"}
    url = reverse("user-create-account")
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 200
    assert list(response.json().keys()) == ["session"]


@pytest.mark.django_db
def test_create_user_profile_cache_timeout(client):
    cache_type = CacheTypes.registration_sms_verification
    payload = {"phone": "+998913665113"}
    phone = payload["phone"]
    session = "Sdadasdada"
    code = 123456
    url = reverse("user-create-account")
    cache.set(generate_cache_key(cache_type, phone, session), code, timeout=5)

    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 400
    assert response.json()["phone"] == "SMS is already sent!"


@pytest.mark.django_db
def test_create_user_profile_without_phone(client):

    payload = {
        "full_name": "Samandar",
    }
    url = reverse("user-create-account")
    response = client.post(url, data=payload, content_type="application/json")

    assert response.status_code == 400
    assert response.json()["phone"] == ["This field is required."]


@pytest.mark.django_db
def test_create_user_profile_already_existing(client, new_user):

    payload = {
        "phone": new_user.phone,
    }
    url = reverse("user-create-account")
    response = client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 400
    assert response.json()["phone"] == ["User with this Phone number already exists."]
