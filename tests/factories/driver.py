import factory

from apps.driver.models import Driver, DriverStatus


class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Driver

    user = factory.SubFactory("tests.factories.user.UserFactory")

    city = "Namangan"
    tex_passport = "ABC1234567"
    driving_license = "AB1234567"
    car_model = "Gentra"
    car_number = "01717CEA"
    car_category = "Comfort"
    has_air_conditioner = True
    has_baggage = True
    smoking_allowed = False
    # driver status
    status = DriverStatus.ACTIVE
    is_online = True
    balance = 50000
