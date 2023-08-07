import factory

from apps.driver.models import CarCategory
from apps.order.models import Order


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    client = factory.SubFactory("tests.factories.user.UserFactory")

    pick_up_address = factory.SubFactory("tests.factories.location.LocationFactory")
    drop_off_address = factory.SubFactory("tests.factories.location.LocationFactory")
    status = Order.OrderStatus.REQUESTED

    car_category = CarCategory.COMFORT
    price = factory.Faker("pyint", min_value=1000)
    number_of_people = 1
    front_right = True
    back_left = False
    back_middle = False
    back_right = False
    type = Order.OrderType.PERSON
    delivery_user_phone = "+998913665113"
    delivery_type = "document"
    approximate_leave_time = factory.Faker("date")
    comment = factory.Faker("word")
    has_air_conditioner = True
    has_baggage = True
    smoking_allowed = False
    promocode = None
