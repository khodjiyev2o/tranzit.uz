from django.db import models


class NamanganBoundaries(models.FloatField):
    min_latitude = 40.61
    max_latitude = 41.00
    min_longitude = 70.81
    max_longitude = 71.67


class TashkentBoundaries(models.FloatField):
    min_latitude = 41.13
    max_latitude = 41.51
    min_longitude = 69.05
    max_longitude = 69.55
