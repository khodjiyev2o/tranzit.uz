from django.urls import path

from .api_endpoints import order, payme

app_name = "payment"

urlpatterns = [
    # create course order
    #path("CourseOrderCreate", order.CourseOrderCreateAPIView.as_view(), name="course-order-create"),

    # path(
    #     "GetLastTransactionStatus/<int:order_id>",
    #     order.GetLastTransactionStatusAPIView.as_view(),
    #     name="get-last-transaction-status",
    # ),
    # payme
    path("Payme", payme.PaymeAPIView.as_view(), name="payme"),
]