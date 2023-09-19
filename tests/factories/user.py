import factory

from apps.users.models import User

random_phones = (
    "+998913665113",
    "+998913665112",
    "+998913665111",
    "+998913665110",
)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    full_name = factory.Faker("word")
    phone = factory.Sequence(lambda n: f'+9989{n:08d}')


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    full_name = factory.Faker("word")
    phone = factory.Faker("random_element", elements=random_phones)
    password = "strong_password_123"
    is_active = True
    is_superuser = True
    is_staff = True


__all__ = ["UserFactory", "SuperUserFactory"]
