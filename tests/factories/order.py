import factory

from apps.driver.models import CarCategory
from apps.order.models import Order


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    client = factory.SubFactory("tests.factories.user.UserFactory")

    pick_up_address = factory.SubFactory("tests.factories.location.LocationFactory")
    drop_off_address = factory.SubFactory("tests.factories.location.LocationFactory")
    status = factory.Faker("random_element", elements=Order.OrderStatus.choices)

    car_category = CarCategory.COMFORT
    price = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    seat = Order.Seat.BACK_LEFT
    type = Order.OrderType.PERSON
    delivery_user_phone = "+998913665113"
    approximate_leave_time = factory.Faker("date")
    comment = factory.Faker("word")
    has_air_conditioner = True
    has_baggage = True
    smoking_allowed = False
    promocode = None
