import factory

from apps.order.models import City, Location


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    city = factory.Faker("random_element", elements=City.choices)
    street = factory.Faker("word")
    latitude = factory.Faker("word")
    longitude = factory.Faker("word")
