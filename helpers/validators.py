from django.core.exceptions import ValidationError
from apps.order.models import City
from helpers.regions import NamanganBoundaries, TashkentBoundaries
from django.utils.translation import gettext_lazy as _


def validate_uzb_boundaries(latitude, longitude):
    # Boundaries of Republic of Uzbekistan
    min_latitude = 37.00
    max_latitude = 46.00
    min_longitude = 56.00
    max_longitude = 74.00

    if not (min_latitude <= latitude <= max_latitude) or not (min_longitude <= longitude <= max_longitude):
        raise ValidationError(message={"location": _("The provided location is outside the boundaries of Uzbekistan.")},
                              code="wrong_location")


def define_region_name(latitude, longitude) -> City:
    # Namangan boundaries
    if (NamanganBoundaries.min_latitude <= latitude <= NamanganBoundaries.max_latitude) and (
            NamanganBoundaries.min_longitude <= longitude <= NamanganBoundaries.max_longitude):
        return City.Namangan

    # Tashkent boundaries
    elif (TashkentBoundaries.min_latitude <= latitude <= TashkentBoundaries.max_latitude) and (
            TashkentBoundaries.min_longitude <= longitude <= TashkentBoundaries.max_longitude):
        return City.Tashkent

    else:
        raise ValidationError(message={"location": _("Wrong Location")}, code="wrong_location")


