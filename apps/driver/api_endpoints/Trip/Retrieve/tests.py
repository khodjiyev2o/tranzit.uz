import pytest
from django.urls import reverse

from apps.order.models import Order
from tests.factories import OrderFactory


@pytest.mark.django_db
def test_driver_retrieve_trip(client, new_driver):
    new_order = OrderFactory(
        number_of_people=4,
        front_right=True,
        back_left=True,
        back_middle=True,
        back_right=True,
    )
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    chosen_seats = []
    if new_order.front_right:
        chosen_seats.append("front_right")
    if new_order.back_left:
        chosen_seats.append("back_left")
    if new_order.back_middle:
        chosen_seats.append("back_middle")
    if new_order.back_right:
        chosen_seats.append("back_right")
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."

    url = reverse("driver-trip-retrieve")
    response = client.get(url, **headers)
    assert response.status_code == 200
    assert list(response.json().keys()) == [
        "id",
        "driver",
        "seats",
        "client",
        "delivery",
        "status",
        "pick_up_address",
        "drop_off_address",
        "approximate_leave_time",
    ]
    assert list(response.json()["driver"].keys()) == ["has_air_conditioner", "has_baggage", "smoking_allowed"]
    assert list(response.json()["client"][0].keys()) == [
        "id",
        "client_full_name",
        "client_phone_number",
        "price",
        "seats",
        "approximate_leave_time",
        "pick_up_address",
        "drop_off_address",
    ]
    assert list(response.json()["client"][0]["seats"]) == chosen_seats
    assert response.json()["delivery"] == []


@pytest.mark.django_db
def test_driver_retrieve_trip_two_seats(client, new_driver):
    new_order = OrderFactory(
        number_of_people=2,
        front_right=True,
        back_left=True,
    )
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    chosen_seats = []
    if new_order.front_right:
        chosen_seats.append("front_right")
    if new_order.back_left:
        chosen_seats.append("back_left")
    if new_order.back_middle:
        chosen_seats.append("back_middle")
    if new_order.back_right:
        chosen_seats.append("back_right")
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."

    url = reverse("driver-trip-retrieve")
    response = client.get(url, **headers)
    assert response.status_code == 200
    assert list(response.json().keys()) == [
        "id",
        "driver",
        "seats",
        "client",
        "delivery",
        "status",
        "pick_up_address",
        "drop_off_address",
        "approximate_leave_time",
    ]
    assert list(response.json()["driver"].keys()) == ["has_air_conditioner", "has_baggage", "smoking_allowed"]
    assert list(response.json()["client"][0].keys()) == [
        "id",
        "client_full_name",
        "client_phone_number",
        "price",
        "seats",
        "approximate_leave_time",
        "pick_up_address",
        "drop_off_address",
    ]
    assert list(response.json()["client"][0]["seats"]) == chosen_seats
    assert response.json()["delivery"] == []


@pytest.mark.django_db
def test_driver_retrieve_trip_two_seats_second_case(client, new_driver):
    new_order = OrderFactory(
        number_of_people=2,
        front_right=False,
        back_middle=True,
        back_right=True,
    )
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    chosen_seats = []
    if new_order.front_right:
        chosen_seats.append("front_right")
    if new_order.back_left:
        chosen_seats.append("back_left")
    if new_order.back_middle:
        chosen_seats.append("back_middle")
    if new_order.back_right:
        chosen_seats.append("back_right")
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."

    url = reverse("driver-trip-retrieve")
    response = client.get(url, **headers)
    assert response.status_code == 200
    assert list(response.json().keys()) == [
        "id",
        "driver",
        "seats",
        "client",
        "delivery",
        "status",
        "pick_up_address",
        "drop_off_address",
        "approximate_leave_time",
    ]
    assert list(response.json()["driver"].keys()) == ["has_air_conditioner", "has_baggage", "smoking_allowed"]
    assert list(response.json()["client"][0].keys()) == [
        "id",
        "client_full_name",
        "client_phone_number",
        "price",
        "seats",
        "approximate_leave_time",
        "pick_up_address",
        "drop_off_address",
    ]
    assert list(response.json()["client"][0]["seats"]) == chosen_seats
    assert response.json()["delivery"] == []


@pytest.mark.django_db
def test_driver_retrieve_trip_delivery(client, new_driver):
    new_order = OrderFactory(
        number_of_people=0,
        type=Order.OrderType.DELIVERY,
    )
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."

    url = reverse("driver-trip-retrieve")
    response = client.get(url, **headers)
    assert response.status_code == 200
    assert list(response.json().keys()) == [
        "id",
        "driver",
        "seats",
        "client",
        "delivery",
        "status",
        "pick_up_address",
        "drop_off_address",
        "approximate_leave_time",
    ]
    assert list(response.json()["driver"].keys()) == ["has_air_conditioner", "has_baggage", "smoking_allowed"]
    assert response.json()["client"] == []
    assert list(response.json()["delivery"][0].keys()) == [
        "id",
        "client_phone_number",
        "delivery_user_phone",
        "delivery_type",
        "price",
        "approximate_leave_time",
        "pick_up_address",
        "drop_off_address",
    ]
    assert response.json()["seats"] == {
        "front_right": False,
        "back_left": False,
        "back_middle": False,
        "back_right": False,
    }
