import os
from pathlib import Path

import environ
from django.core.asgi import get_asgi_application


base_dir = Path(__file__).resolve().parent.parent  # noqa
environ.Env().read_env(os.path.join(base_dir, ".env"))  # noqa
django_asgi_app = get_asgi_application()  # noqa

"""
Initialize Django ASGI application early to ensure the AppRegistry
is populated before importing code that may import ORM models.
"""

from channels.routing import ProtocolTypeRouter, URLRouter

import apps.order.routing  # noqa

from .channels_middleware import JwtAuthMiddlewareStack


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JwtAuthMiddlewareStack(URLRouter(apps.order.routing.websocket_urlpatterns)),
    }
)
