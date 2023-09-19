import pytest
from django.urls import reverse

from apps.order.models import Order
from tests.factories import OrderFactory


@pytest.mark.django_db
def test_cancel_order_person(client, new_driver, new_order):
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."

    url = reverse("order-cancel")

    response = client.post(url, data=data, **headers)
    assert response.json()["message"] == "Successfully removed"
    assert response.status_code == 200


@pytest.mark.django_db
def test_cancel_order_person_not_found(client, new_driver):
    new_order = OrderFactory(status=Order.OrderStatus.IN_PROGRESS)
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }

    url = reverse("order-cancel")

    response = client.post(url, data=data, **headers)
    assert response.json()["errors"][0]["code"] == "order_not_found"
    assert response.status_code == 400


@pytest.mark.django_db
def test_cancel_order_delivery(client, new_driver, new_location):
    new_order = OrderFactory(type=Order.OrderType.DELIVERY, pick_up_address=new_location)
    url = reverse("order-accept")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Order added to trip successfully."

    url = reverse("order-cancel")

    response = client.post(url, data=data, **headers)
    assert response.json()["message"] == "Successfully removed"
    assert response.status_code == 200


@pytest.mark.django_db
def test_cancel_order_delivery_not_found(client, new_driver):
    new_order = OrderFactory(status=Order.OrderStatus.IN_PROGRESS, type=Order.OrderType.DELIVERY)
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }

    url = reverse("order-cancel")

    response = client.post(url, data=data, **headers)
    assert response.json()["errors"][0]["code"] == "order_not_found"
    assert response.status_code == 400


@pytest.mark.django_db
def test_cancel_order_not_found_serialize_wrong_pk(client, new_driver):
    OrderFactory(status=Order.OrderStatus.IN_PROGRESS, type=Order.OrderType.DELIVERY)
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": 1234455,
    }

    url = reverse("order-cancel")

    response = client.post(url, data=data, **headers)
    assert response.json()["errors"][0]["code"] == "order_not_found"
    assert response.status_code == 400


@pytest.mark.django_db
def test_cancel_order_not_found_serializer_wrong_status(client, new_driver):
    new_order = OrderFactory(status=Order.OrderStatus.COMPLETED, type=Order.OrderType.DELIVERY)
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    data = {
        "order": new_order.id,
    }

    url = reverse("order-cancel")

    response = client.post(url, data=data, **headers)
    assert response.json()["errors"][0]["code"] == "order_not_found"
    assert response.status_code == 400
