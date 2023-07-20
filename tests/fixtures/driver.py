import pytest
from pytest_factoryboy import register

from tests.factories import DriverFactory


register(DriverFactory)


@pytest.fixture()
def new_driver(db, driver_factory):
    return driver_factory.create()
