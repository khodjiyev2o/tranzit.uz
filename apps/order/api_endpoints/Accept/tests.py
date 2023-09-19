import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse

from apps.order.models import Order
from tests.factories import LocationFactory, OrderFactory


@pytest.mark.django_db
def test_accept_order(client, new_driver, new_order):
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."


@pytest.mark.django_db
def test_accept_order_not_found(client, new_driver, new_order):
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": 1234,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 400
    assert response.json()['errors'][0]['code'] == "order_not_found"


@pytest.mark.django_db
def test_accept_order_four_people(client, new_driver):
    new_order = OrderFactory(number_of_people=4, front_right=True, back_left=True, back_middle=True, back_right=True)
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."


@pytest.mark.django_db
def test_accept_order_different_location_conflict_person(client, new_driver):
    new_location = LocationFactory(city="Tashkent")
    new_order = OrderFactory(
        number_of_people=3, front_right=True, back_left=True, back_middle=True, pick_up_address=new_location
    )
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."

    # 1st case - failure - person
    new_location = LocationFactory(city="Namangan")
    new_order = OrderFactory(
        number_of_people=1,
        front_right=True,
        pick_up_address=new_location,
    )
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.json()["errors"][0]['message'] == \
           "All client orders and deliveries should have the same pick-up address."
    assert response.status_code == 400


@pytest.mark.django_db
def test_accept_order_different_location_conflict_delivery(client, new_driver):
    new_location = LocationFactory(city="Tashkent")
    new_order = OrderFactory(
        type=Order.OrderType.DELIVERY,
        pick_up_address=new_location,
    )
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."

    # 1st case - failure - delivery
    new_location = LocationFactory(city="Namangan")
    new_order = OrderFactory(
        type=Order.OrderType.DELIVERY,
        pick_up_address=new_location,
    )
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.json()["errors"][0]['message'] == \
           "All client orders and deliveries should have the same pick-up address."
    assert response.status_code == 400


@pytest.mark.django_db
def test_accept_order_three_people(client, new_driver):
    new_order = OrderFactory(
        number_of_people=3,
        front_right=True,
        back_left=True,
        back_middle=True,
    )
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."


@pytest.mark.django_db
def test_accept_order_two_people(client, new_driver):
    new_order = OrderFactory(number_of_people=2, front_right=True, back_right=True)
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.json()["message"] == "Order added to trip successfully."
    assert response.status_code == 200


@pytest.mark.django_db
def test_accept_order_conflicting_seats(client, new_driver, new_location):
    new_order = OrderFactory(number_of_people=2, front_right=True, back_right=True, pick_up_address=new_location)
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."

    # 1st case - failure
    new_order = OrderFactory(
        number_of_people=1,
        front_right=True,
        pick_up_address=new_location,
    )
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.json()["errors"][0]['message'] == "Seats conflict with another order"
    assert response.status_code == 400

    # 2nd case - failure
    new_order = OrderFactory(
        pick_up_address=new_location,
        number_of_people=1,
        back_right=True,
        front_right=False,  # default=True
    )
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.json()["errors"][0]['message'] == "Seats conflict with another order"
    assert response.status_code == 400

    # 3rd case - success
    new_order = OrderFactory(
        pick_up_address=new_location,
        number_of_people=2,
        back_middle=True,
        back_left=True,
        front_right=False,
    )
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.json()["message"] == "Order added to trip successfully."
    assert response.status_code == 200

    # 4rd case(delivery) - success
    new_order = OrderFactory(
        pick_up_address=new_location,
        type=Order.OrderType.DELIVERY,
    )
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.json()["message"] == "Order added to trip successfully."
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_manager_without_delivery_phone(new_user):
    with pytest.raises(ValidationError) as exception_info:
        Order.objects.create(type=Order.OrderType.DELIVERY, client=new_user, approximate_leave_time="2022-10-12")

    assert (
        str(exception_info.value.message_dict["__all__"][0])
        == "Phone number and delivery type is required for delivery orders."
    )


@pytest.mark.django_db
def test_order_manager_number_of_people_conflict(new_user):
    with pytest.raises(ValidationError) as exception_info:
        Order.objects.create(type=Order.OrderType.PERSON, client=new_user, approximate_leave_time="2022-10-12")

    assert str(exception_info.value.message_dict["__all__"][0]) == "For 1 person, 1 seats must be selected."
