import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_list_order_view(client, new_driver, new_order):
    url = reverse("order-list")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_driver.user.tokens.get('access')}"}
    response = client.get(url, **headers)
    assert response.status_code == 200
    assert response.json()[0]["id"] == new_order.id
    assert response.json()[0]["client"]["full_name"] == new_order.client.full_name
    assert response.json()[0]["client"]["phone"] == str(new_order.client.phone)
    assert response.json()[0]["seat"] == new_order.seat
    assert response.json()[0]["pick_up_address"]["city"] == str(new_order.pick_up_address.city)
    assert response.json()[0]["drop_off_address"]["city"] == str(new_order.drop_off_address.city)
    assert response.json()[0]["pick_up_address"]["street"] == new_order.pick_up_address.street
    assert response.json()[0]["drop_off_address"]["street"] == new_order.drop_off_address.street
    assert response.json()[0]["price"] == new_order.price
