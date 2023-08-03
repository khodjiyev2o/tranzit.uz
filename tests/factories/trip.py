import factory

from apps.order.models import Trip
from tests.factories.order import OrderFactory


class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trip

    driver = factory.SubFactory("tests.factories.driver.DriverFactory")
    client = factory.RelatedFactoryList(OrderFactory, size=4)
    delivery = factory.RelatedFactoryList(
        OrderFactory,
        size=4,
    )
    status = Trip.TripStatus.ACTIVE
