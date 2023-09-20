from .base import *  # noqa


STAGE = "development"
DEBUG = True
TEST = False

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": (BASE_DIR / "db.sqlite3"),
    }
}
