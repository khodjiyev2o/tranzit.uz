from django.db import transaction as db_transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.payment.api_endpoints.payme.auth import AUTH_ERROR, authentication
from apps.payment.api_endpoints.payme.provider import PaymeProvider
from apps.payment.models import Provider, Transaction, TransactionStatus
from apps.payment.views import PaymentView

from .serializers import PaymeSerializer
from .utils import PaymeMethods


class PaymeAPIView(PaymentView):
    permission_classes = [AllowAny]
    http_method_names = ["post"]
    authentication_classes = []  # type: ignore
    TYPE = ""
    PROVIDER = Provider.PAYME  # type: ignore

    def __init__(self):
        self.METHODS = {
            PaymeMethods.CHECK_PERFORM_TRANSACTION: self.check_perform_transaction,
            PaymeMethods.CREATE_TRANSACTION: self.create_transaction,
            PaymeMethods.PERFORM_TRANSACTION: self.perform_transaction,
            PaymeMethods.CHECK_TRANSACTION: self.check_transaction,
            PaymeMethods.CANCEL_TRANSACTION: self.cancel_transaction,
        }
        self.params = None
        super(PaymeAPIView, self).__init__()

    @swagger_auto_schema(request_body=PaymeSerializer)
    def post(self, request, *args, **kwargs):
        check = authentication(request)

        if check is False or not check:
            return Response(AUTH_ERROR)

        serializer = PaymeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)

        method = serializer.validated_data["method"]
        self.params = serializer.validated_data["params"]
        self.TYPE = method

        with db_transaction.atomic():
            response_data = self.METHODS[method]()

        return Response(response_data)

    def check_perform_transaction(self):
        error, error_message, code = PaymeProvider(self.params).check_perform_transaction()
        if error:
            return dict(error=dict(code=code, message=error_message))
        return dict(result=dict(allow=True))

    def create_transaction(self):
        error, error_message, code = PaymeProvider(self.params).create_transaction()

        # when order is not found
        if error and code == PaymeProvider.ORDER_NOT_FOUND:
            return dict(error=dict(code=code, message=error_message))

        transaction = (
            Transaction.objects.filter(order__driver__user__phone=self.params["account"]["phone"], transaction_id=self.params["id"])
            .order_by("-id")
            .first()
        )

        if not transaction:
            return dict(error=dict(code=code, message=error_message))

        # when order found and transaction created but error occurred
        if error:
            transaction.status = TransactionStatus.FAILED
            transaction.save()
            return dict(error=dict(code=code, message=error_message))

        return dict(
            result=dict(
                create_time=int(transaction.created_at.timestamp() * 1000),
                transaction=transaction.transaction_id,
                state=PaymeProvider.CREATE_TRANSACTION,
            )
        )

    def perform_transaction(self):
        error, error_message, code = PaymeProvider(self.params).perform_transaction()
        # when order is not found
        if error and (code == PaymeProvider.ORDER_NOT_FOUND or code == PaymeProvider.TRANSACTION_NOT_FOUND):
            return dict(error=dict(code=code, message=error_message))

        transaction = Transaction.objects.get(transaction_id=self.params["id"], order__provider=Provider.PAYME)

        # when order found and transaction created but error occurred
        if error:
            transaction.status = TransactionStatus.FAILED
            transaction.save()
            return dict(error=dict(code=code, message=error_message))

        if transaction.status == TransactionStatus.WAITING:
            with db_transaction.atomic():
                transaction.apply()

        return dict(
            result=dict(
                transaction=transaction.transaction_id,
                perform_time=int(transaction.paid_at.timestamp() * 1000),
                state=PaymeProvider.CLOSE_TRANSACTION,
            )
        )

    def check_transaction(self):
        error, error_message, code = PaymeProvider(self.params).check_transaction()
        if error:
            return dict(error=dict(code=code, message=error_message))

        transaction = Transaction.objects.get(transaction_id=self.params["id"], order__provider=Provider.PAYME)
        perform_time = int(transaction.paid_at.timestamp() * 1000) if transaction.paid_at else 0
        cancel_time = int(transaction.cancel_time.timestamp() * 1000) if transaction.cancel_time else 0
        reason = None
        if transaction.status == TransactionStatus.PAID:
            state = PaymeProvider.CLOSE_TRANSACTION
        elif transaction.status == TransactionStatus.CANCELED:
            state = PaymeProvider.CANCEL_TRANSACTION_CODE
            reason = 3
        else:
            state = PaymeProvider.CREATE_TRANSACTION

        return dict(
            result=dict(
                create_time=int(transaction.created_at.timestamp() * 1000),
                perform_time=perform_time,
                cancel_time=cancel_time,
                transaction=str(transaction.transaction_id),
                state=state,
                reason=reason,
            )
        )

    def cancel_transaction(self):
        error, error_message, code = PaymeProvider(self.params).cancel_transaction()
        if error:
            return dict(error=dict(code=code, message=error_message))
        transaction = Transaction.objects.get(transaction_id=self.params["id"], order__provider=Provider.PAYME)
        if transaction.status != TransactionStatus.CANCELED:
            transaction.cancel()

        perform_time = int(transaction.paid_at.timestamp() * 1000) if transaction.paid_at else 0
        cancel_time = int(transaction.cancel_time.timestamp() * 1000) if transaction.cancel_time else 0
        return dict(
            result=dict(
                create_time=int(transaction.created_at.timestamp() * 1000),
                perform_time=perform_time,
                cancel_time=cancel_time,
                transaction=str(transaction.transaction_id),
                state=PaymeProvider.CANCEL_TRANSACTION_CODE,
                reason=3,
            )
        )
