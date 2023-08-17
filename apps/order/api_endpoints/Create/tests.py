import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse

from apps.order.models import Order
from apps.driver.models import CarCategory
from tests.factories import LocationFactory, OrderFactory


@pytest.mark.django_db
def test_create_order(client, new_user, new_order, new_location):
    url = reverse("order-create")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {new_user.tokens.get('access')}"}

    data = {
        "pick_up_address": {
                'city': 'Namangan',
                'street': 'Olmazor',
                'latitude': '12133333.22',
                'longitude': '32232.333',
            },
        "drop_off_address": {
                'city': 'Tashkent',
                'street': 'Samarqand Darvoza 2',
                'latitude': '12133333.22',
                'longitude': '32232.333',
            },
        "car_category": CarCategory.COMFORT,
        "price": 120000,
        "number_of_people": 1,
        "front_right": True,
        "back_left": False,
        "back_middle": False,
        "back_right": False,
        "type": Order.OrderType.PERSON,
        "approximate_leave_time": "2022-06-10-19:00",
        "comment": "something_comment",
        "has_air_conditioner": True,
        "has_baggage": True,
        "smoking_allowed": False,
        }
    response = client.post(url, data=data, **headers, content_type="application/json")

    assert response.status_code == 201
    assert response.json()['pick_up_address'] == data['pick_up_address']
    assert response.json()['car_category'] == data['car_category']
    assert response.json()['number_of_people'] == data['number_of_people']
    assert response.json()['front_right'] == data['front_right']
    assert response.json()['back_left'] == data['back_left']
    assert response.json()['back_middle'] == data['back_middle']
    assert response.json()['back_right'] == data['back_right']
    assert response.json()['type'] == data['type']
    assert response.json()['has_air_conditioner'] == data['has_air_conditioner']
    assert response.json()['has_baggage'] == data['has_baggage']
    assert response.json()['smoking_allowed'] == data['smoking_allowed']
