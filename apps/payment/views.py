# Create your views here.
from rest_framework.views import APIView

from django.db import transaction

from apps.payment.models import PaymentMerchantRequestLog


class PaymentView(APIView):
    TYPE: str = ""
    PROVIDER: str = ""

    @transaction.non_atomic_requests
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        PaymentMerchantRequestLog.objects.create(
            header=self.request.headers,
            body=self.request.data,
            method=self.request.method,
            type=self.TYPE,
            response=response.data,
            response_status_code=response.status_code,
            provider=self.PROVIDER,
        )
        return response
