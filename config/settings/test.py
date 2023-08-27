from .base import *  # noqa


DEBUG = False
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": (BASE_DIR / "db.sqlite3"),
    }
}
TEST = env.str("TEST", True)
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# for github actions ci/cd
if TEST:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://localhost:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }