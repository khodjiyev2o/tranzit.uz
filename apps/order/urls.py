from django.urls import path

from apps.order.api_endpoints import (
    GetDeliveryOrderPriceAPIView,
    GetOrderPriceAPIView,
    OrderAcceptView,
    OrderCancelView,
    OrderCreateView,
    OrderDetailView,
    OrderListView,
    PromocodeRetrieveView,
    UserOrderCancelView,
    UserOrderListView,
)


urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("user-order-list/", UserOrderListView.as_view(), name="user-order-list"),
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("accept/", OrderAcceptView.as_view(), name="order-accept"),
    path("cancel/", OrderCancelView.as_view(), name="order-cancel"),
    path("user-cancel/", UserOrderCancelView.as_view(), name="user-order-cancel"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("promocode/<str:code>/", PromocodeRetrieveView.as_view(), name="promocode-retrieve"),
    path("get-price/", GetOrderPriceAPIView.as_view(), name="order-get-price"),
    path("get-delivery-price/", GetDeliveryOrderPriceAPIView.as_view(), name="order-get-price-delivery"),
]
