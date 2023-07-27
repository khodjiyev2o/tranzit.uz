import pytest
from pytest_factoryboy import register

from tests.factories import TripFactory


register(TripFactory)


@pytest.fixture()
def new_trip(db, trip_factory):
    return trip_factory.create()
