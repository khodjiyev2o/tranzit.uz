import pytest

from apps.order.models import Location, Order, Trip


@pytest.mark.django_db
def test_location_model_str_method(client, new_location):
    assert Location.__str__(new_location) == f"{new_location.city} | {new_location.street}"


@pytest.mark.django_db
def test_order_model_str_method(client, new_order):

    assert Order.__str__(new_order) == f"{new_order.client.full_name} | {new_order.pick_up_address.street}"

@pytest.mark.django_db
def test_trip_model_str_method(client, new_trip):
        assert Trip.__str__(new_trip) == f"{new_trip.driver.user.full_name} | {new_trip.status}"
