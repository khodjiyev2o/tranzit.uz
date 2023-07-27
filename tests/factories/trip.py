import factory

from apps.order.models import Trip
from tests.factories.order import OrderFactory


class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trip

    driver = factory.SubFactory("tests.factories.driver.DriverFactory")
    front_right_seat = factory.SubFactory("tests.factories.order.OrderFactory")
    back_left_seat = factory.SubFactory("tests.factories.order.OrderFactory")
    back_middle_seat = factory.SubFactory("tests.factories.order.OrderFactory")
    back_right_seat = factory.SubFactory("tests.factories.order.OrderFactory")
    delivery = factory.RelatedFactoryList(
        OrderFactory,
        size=4,
    )
    status = Trip.TripStatus.ACTIVE
