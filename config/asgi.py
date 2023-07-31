import os
from pathlib import Path

import environ
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.order.urls import websocket_urlpatterns
from .channels_middleware import JwtAuthMiddlewareStack

base_dir = Path(__file__).resolve().parent.parent
environ.Env().read_env(os.path.join(base_dir, ".env"))


django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JwtAuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
