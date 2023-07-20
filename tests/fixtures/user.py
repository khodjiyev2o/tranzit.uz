import pytest
from pytest_factoryboy import register

from tests.factories import SuperUserFactory, UserFactory


register(UserFactory)
register(SuperUserFactory)


@pytest.fixture()
def new_user(db, user_factory):
    return user_factory.create()


@pytest.fixture()
def new_admin_user(db, super_user_factory):
    return super_user_factory.create()
