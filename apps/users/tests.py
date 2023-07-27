import pytest

from apps.driver.models import Driver
from apps.users.models import User


@pytest.mark.django_db
def test_user_manager(client):
    User.objects.create_user(phone="+998913665113", full_name="Samandar")

    assert User.objects.count() == 1


@pytest.mark.django_db
def test_user_manager_without_phone():
    with pytest.raises(ValueError) as exception_info:
        User.objects.create_user(full_name="samandarkhodjiyev@gmail.com", phone=None)

    assert str(exception_info.value) == "User must have a phone!"


@pytest.mark.django_db
def test_superuser_manager(client):
    User.objects.create_superuser(phone="+998913665113", password="some_passowrd1234")
    assert User.objects.filter(is_superuser=True).count() == 1


@pytest.mark.django_db
def test_create_superuser():
    with pytest.raises(ValueError) as exception_info:
        User.objects.create_superuser(phone="+998913665113", password=None)

    assert str(exception_info.value) == "Super User must have  password!"


@pytest.mark.django_db
def test_user_tokens(client):
    new_user = User.objects.create_superuser(phone="+998913665113", password="some_passowrd1234")
    assert User.objects.filter(is_superuser=True).count() == 1
    assert list(new_user.tokens.keys()) == ["access", "refresh"]


@pytest.mark.django_db
def test_user_model_str_method(client):

    new_user = User.objects.create(phone="+998913655113")
    assert User.__str__(new_user) == new_user.phone


@pytest.mark.django_db
def test_driver_model_str_method(client, new_driver):

    assert Driver.__str__(new_driver) == f"Driver| {new_driver.user.full_name} - {new_driver.balance}"
