import pytest
from pytest_factoryboy import register

from tests.factories import LocationFactory


register(LocationFactory)


@pytest.fixture()
def new_location(db, location_factory):
    return location_factory.create()
