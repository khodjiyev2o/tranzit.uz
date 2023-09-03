from django.urls import path

from apps.order.consumers import ChatConsumer


websocket_urlpatterns = [
    path(r"ws/driver/connect/", ChatConsumer.as_asgi()),
]
