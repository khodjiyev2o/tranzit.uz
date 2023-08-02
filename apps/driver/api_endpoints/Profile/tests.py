import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_profile(client, new_driver):
    url = reverse("driver-profile-retrieve-update")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    response = client.get(url, **headers)
    assert response.status_code == 200
    assert response.json()["user"]["full_name"] == new_driver.user.full_name
    assert response.json()["user"]["photo"] == new_driver.user.photo
    assert response.json()["user"]["phone"] == str(new_driver.user.phone)
    assert response.json()["balance"] == new_driver.balance
