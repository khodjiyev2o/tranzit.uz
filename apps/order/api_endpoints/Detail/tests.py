import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_list_order_view(client, new_driver, new_order):
    url = reverse("order-detail", kwargs={"pk": new_order.pk})
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    response = client.get(url, **headers)
    assert response.status_code == 200
    assert list(response.json().keys()) == [
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
        "delivery_type",
    ]
    assert response.json()["id"] == new_order.id
    assert response.json()["client"]["full_name"] == new_order.client.full_name
    assert response.json()["client"]["phone"] == str(new_order.client.phone)
    assert response.json()["back_left"] == new_order.back_left
    assert response.json()["back_middle"] == new_order.back_middle
    assert response.json()["back_right"] == new_order.back_right
    assert response.json()["front_right"] == new_order.front_right
    assert response.json()["pick_up_address"]["city"] == str(new_order.pick_up_address.city)
    assert response.json()["drop_off_address"]["city"] == str(new_order.drop_off_address.city)
    assert response.json()["pick_up_address"]["street"] == new_order.pick_up_address.street
    assert response.json()["drop_off_address"]["street"] == new_order.drop_off_address.street
    assert response.json()["price"] == new_order.price
    assert response.json()["delivery_user_phone"] == new_order.delivery_user_phone
    assert response.json()["delivery_type"] == new_order.delivery_type
