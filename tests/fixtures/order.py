import pytest
from pytest_factoryboy import register

from tests.factories import OrderFactory


register(OrderFactory)


@pytest.fixture()
def new_order(db, order_factory):
    return order_factory.create()
