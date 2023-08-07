import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_driver_update_profile(client, new_driver):
    url = reverse("driver-profile-update")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {"full_name": "Samandar"}
    response = client.put(url, data=data, **headers, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["full_name"] == data["full_name"]
    assert response.json()["photo"] == new_driver.user.photo
