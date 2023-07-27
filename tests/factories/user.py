import factory

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    full_name = factory.Faker("word")
    phone = factory.Faker("random_number", digits=13)


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    full_name = factory.Faker("word")
    phone = factory.Faker("random_number", digits=13)
    password = "strong_password_123"
    is_active = True
    is_superuser = True
    is_staff = True


__all__ = ["UserFactory", "SuperUserFactory"]
