# chat/urls.py
from django.urls import path, re_path

from apps.driver.api_endpoints import index
from apps.order.api_endpoints import OrderListView
from apps.order.consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(r"ws/driver/connect/", ChatConsumer.as_asgi()),
]

urlpatterns = [
    path("template", index, name="index"),
    path("", OrderListView.as_view(), name="order-list"),
]
