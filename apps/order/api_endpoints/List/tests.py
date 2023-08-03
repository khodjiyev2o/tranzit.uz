import pytest
from django.urls import reverse

from apps.driver.models import DriverStatus
from tests.factories import DriverFactory


@pytest.mark.django_db
def test_list_order_view(client, new_driver, new_order):
    url = reverse("order-list")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    response = client.get(url, **headers)
    assert response.status_code == 200
    assert list(response.json()[0].keys()) == [
        "id",
        "approximate_leave_time",
        "client",
        "number_of_people",
        "front_right",
        "back_left",
        "back_middle",
        "back_right",
        "pick_up_address",
        "drop_off_address",
        "price",
        "type",
        "delivery_user_phone",
    ]
    assert response.json()[0]["id"] == new_order.id
    assert response.json()[0]["client"]["full_name"] == new_order.client.full_name
    assert response.json()[0]["client"]["phone"] == str(new_order.client.phone)
    assert response.json()[0]["back_left"] == new_order.back_left
    assert response.json()[0]["pick_up_address"]["city"] == str(new_order.pick_up_address.city)
    assert response.json()[0]["drop_off_address"]["city"] == str(new_order.drop_off_address.city)
    assert response.json()[0]["pick_up_address"]["street"] == new_order.pick_up_address.street
    assert response.json()[0]["drop_off_address"]["street"] == new_order.drop_off_address.street
    assert response.json()[0]["price"] == new_order.price


@pytest.mark.django_db
def test_list_order_view_no_enough_balance(client, new_order):
    new_driver = DriverFactory(balance=1000)
    url = reverse("order-list")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    response = client.get(url, **headers)
    assert response.json()["detail"] == "Driver does not have enough balance"


@pytest.mark.django_db
def test_list_order_view_in_moderation(client, new_order):
    new_driver = DriverFactory(balance=10000, status=DriverStatus.IN_MODERATION)
    url = reverse("order-list")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    response = client.get(url, **headers)
    assert response.json()["detail"] == "Driver is in moderation"


@pytest.mark.django_db
def test_list_order_view_no_driver(client, new_order, new_user):
    url = reverse("order-list")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_user.tokens.get('access')}"}
    response = client.get(url, **headers)
    assert response.json()["detail"] == "User is not a driver"
