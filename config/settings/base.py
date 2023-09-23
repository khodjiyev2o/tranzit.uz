import os
from datetime import timedelta
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

from config.jazzmin_conf import *  # noqa


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# READING ENV
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))


SECRET_KEY = env.str("SECRET_KEY")
DEBUG = True

ALLOWED_HOSTS = ["*"]

LOCAL_APPS = [
    "apps.users.apps.UsersConfig",
    "apps.common.apps.CommonConfig",
    "apps.driver.apps.DriverConfig",
    "apps.order.apps.OrderConfig",
    "apps.payment.apps.PaymentConfig",
]
THIRD_PARTY_APPS = [
    "daphne",
    "modeltranslation",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "django_filters",
    "debug_toolbar",
]
DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DJANGO_APPS

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
AUTH_USER_MODEL = "users.User"
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


TIME_ZONE = "Asia/Tashkent"

# LANGUAGE SETTINGS
LANGUAGE_CODE = "en"
USE_I18N = True
USE_TZ = True
USE_L10N = True

LANGUAGES = [
    ("uz", _("Uzbek")),
    ("en", _("English")),
    ("ru", _("Russian")),
]
MODELTRANSLATION_LANGUAGES_CHOICES = (
    ("uz", _("Uzbek")),
    ("en", _("English")),
    ("ru", _("Russian")),
)
MODELTRANSLATION_LANGUAGES = ("uz", "ru", "en")
MODELTRANSLATION_DEFAULT_LANGUAGE = "uz"
MODELTRANSLATION_FALLBACK_LANGUAGES = ("uz", "ru", "en")
LOCALE_PATHS = (os.path.join(BASE_DIR, " locale"),)

# STATIC AND MEDIA SETTINGS
STATIC_URL = "staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = (BASE_DIR / "static",)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "EXCEPTION_HANDLER": "helpers.exception_handler.custom_exception_handler",
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=99),
    "ROTATE_REFRESH_TOKENS": True,
}

# SWAGGER SETTINGS
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"api_key": {"type": "apiKey", "in": "header", "name": "Authorization"}},
}


# CACHES
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{env.str('REDIS_URL', 'redis://localhost:6379/0')}",
        "KEY_PREFIX": "tranzit-backend",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# CHANNELS
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env.str("CELERY_BROKER_URL", "redis://localhost:6379")],
        },
    },
}

# PAYMENT SETTINGS
PROVIDERS = {
    "payme": {
        "merchant_id": env.str("PAYME_MERCHANT_ID", "64e3133940e7b5db6310d605"),
        "secret_key": env.str("PAYME_SECRET_KEY", "cR2D6qaN9mVTmNYKrovpVQt?BWDMOzgrr%JS"),
        "test_secret_key": env.str("PAYME_TEST_SECRET_KEY", "Dec%o4b%oKvERKPPOxu&pigeNWHe8VOzDs?N"),
    },
    "click": {
        "url": "https://my.click.uz/services/pay",
        "merchant_id": env.str("CLICK_MERCHANT_ID", ""),
        "merchant_service_id": env.str("CLICK_MERCHANT_SERVICE_ID", ""),
        "merchant_user_id": env.str("CLICK_MERCHANT_USER_ID", ""),
        "secret_key": env.str("CLICK_SECRET_KEY", ""),
    },
    "karmon_pay": {
        "api_key": env.str("KARMON_PAY_API_KEY", ""),
    },
    "uzum_bank": {
        "service_id": env.str("UZUM_BANK_SERVICE_ID", ""),
        "cash_id": env.str("UZUM_BANK_CASH_ID", ""),
        "username": env.str("UZUM_BANK_USERNAME", ""),
        "password": env.str("UZUM_BANK_PASSWORD", ""),
    },
}


# COMPANY SETTINGS
TRANSIT_SERVICE_FEE = 0.05
TRANSIT_DRIVER_MINIMUM_BALANCE = 30000
PRICING_RULES = {
    "front_right": 140000,
    "back_left": 120000,
    "back_right": 120000,
    "back_middle": 110000,
}
DISCOUNT_PRICE_FOR_ADDITIONAL_PERSON = 5000
