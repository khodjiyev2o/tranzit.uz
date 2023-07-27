import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_user_update_profile(client, new_user):
    payload = {"full_name": "Samandar"}
    url = reverse("user-retrieve-update")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_user.tokens.get('access')}"}
    response = client.put(url, data=payload, **headers, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["full_name"] == payload["full_name"]
    assert response.json()["photo"] == new_user.photo
    assert response.json()["phone"] == str(new_user.phone)
    assert list(response.json().keys()) == ["full_name", "photo", "phone"]


@pytest.mark.django_db
def test_user_get_profile(client, new_user):
    url = reverse("user-retrieve-update")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_user.tokens.get('access')}"}
    response = client.get(url, **headers, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["full_name"] == new_user.full_name
    assert response.json()["photo"] is None
    assert response.json()["phone"] == str(new_user.phone)
    assert list(response.json().keys()) == ["full_name", "photo", "phone"]
