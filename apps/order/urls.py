from django.urls import path

from apps.driver.api_endpoints import index
from apps.order.api_endpoints import (
    OrderAcceptView,
    OrderCancelView,
    OrderCreateView,
    OrderDetailView,
    OrderListView,
)


urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("template/", index, name="index"),
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("accept/", OrderAcceptView.as_view(), name="order-accept"),
    path("cancel/", OrderCancelView.as_view(), name="order-cancel"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
