from django.db import models


class NamanganBoundaries(models.FloatField):
    min_latitude = 40.21
    max_latitude = 41.02
    min_longitude = 70.81
    max_longitude = 71.69


class TashkentBoundaries(models.FloatField):
    min_latitude = 41.13
    max_latitude = 41.71
    min_longitude = 69.05
    max_longitude = 69.85
