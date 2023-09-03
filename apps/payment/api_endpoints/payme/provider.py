from django.utils import timezone

from apps.payment.models import Order, Provider, Transaction, TransactionStatus


class PaymeProvider:
    ORDER_NOT_FOUND = -31050
    ORDER_ALREADY_PAID = -31051
    ORDER_INVALID_PAYMENT_TYPE = -31053
    TRANSACTION_NOT_FOUND = -31054
    INVALID_AMOUNT = -31001
    UNABLE_TO_PERFORM_OPERATION = -31008

    CREATE_TRANSACTION = 1
    CLOSE_TRANSACTION = 2
    CANCEL_TRANSACTION_CODE = -1
    PERFORM_CANCELED_CODE = -2

    ORDER_NOT_FOND_MESSAGE = {"uz": "Buyurtma topilmadi", "ru": "Заказ не найден", "en": "Order not fond"}
    ORDER_ALREADY_PAID_MESSAGE = {
        "uz": "Buyurtma allaqachon to'langan",
        "ru": "Заказ уже оплачен",
        "en": "Order already paid",
    }
    ORDER_INVALID_PAYMENT_TYPE_MESSAGE = {
        "uz": "To'lov usuli noto'g'ri",
        "ru": "Неверный тип оплаты",
        "en": "Invalid payment type",
    }
    TRANSACTION_NOT_FOUND_MESSAGE = {
        "uz": "Tranzaksiya topilmadi",
        "ru": "Транзакция не найдена",
        "en": "Transaction not found",
    }
    UNABLE_TO_PERFORM_OPERATION_MESSAGE = {
        "uz": "Ushbu amalni bajarib bo'lmaydi",
        "ru": "Невозможно выполнить данную операцию",
        "en": "Unable to perform operation",
    }

    INVALID_AMOUNT_MESSAGE = {"uz": "Miqdori notog'ri", "ru": "Неверная сумма", "en": "Invalid amount"}

    def __init__(self, params):
        self.params = params
        self.code = None
        self.error = None
        self.error_message = None
        self.order = self.get_order()

    def perform_transaction(self):
        try:
            transaction = Transaction.objects.get(transaction_id=self.params["id"], order__provider=Provider.PAYME)
        except Transaction.DoesNotExist:
            return True, self.TRANSACTION_NOT_FOUND_MESSAGE, self.TRANSACTION_NOT_FOUND
        if transaction.status == TransactionStatus.FAILED:
            return True, self.UNABLE_TO_PERFORM_OPERATION, self.UNABLE_TO_PERFORM_OPERATION_MESSAGE
        if (
            Transaction.objects.filter(order=transaction.order, status=TransactionStatus.PAID)
            .exclude(transaction_id=transaction.transaction_id)
            .exists()
        ):
            self.order = transaction.order
            self.validate_order()

        return self.error, self.error_message, self.code

    def check_transaction(self):
        try:
            Transaction.objects.get(transaction_id=self.params["id"], order__provider=Provider.PAYME)
        except Transaction.DoesNotExist:
            return True, self.TRANSACTION_NOT_FOUND_MESSAGE, self.TRANSACTION_NOT_FOUND

        return self.error, self.error_message, self.code

    def create_transaction(self):
        if not self.order:
            return True, self.ORDER_NOT_FOND_MESSAGE, self.ORDER_NOT_FOUND

        _time = timezone.now() - timezone.timedelta(seconds=15)
        check_transaction = Transaction.objects.filter(
            order=self.order, order__provider=Provider.PAYME, status=TransactionStatus.WAITING, created_at__gte=_time
        ).order_by("-id")

        if check_transaction and check_transaction.first().transaction_id != self.params["id"]:
            return True, self.TRANSACTION_NOT_FOUND_MESSAGE, self.TRANSACTION_NOT_FOUND

        transaction, _ = Transaction.objects.get_or_create(
            transaction_id=self.params["id"],
            order=self.order,
            defaults={"amount": self.params["amount"] / 100, "status": TransactionStatus.WAITING},
        )
        self.validate_order()
        self.validate_amount(self.params["amount"] / 100)
        return self.error, self.error_message, self.code

    def check_perform_transaction(self):
        if not self.order:
            return True, self.ORDER_NOT_FOND_MESSAGE, self.ORDER_NOT_FOUND

        self.validate_order()
        self.validate_amount(self.params["amount"] / 100)

        return self.error, self.error_message, self.code

    def get_order(self):
        if not self.params.get("account"):
            return
        try:
            return Order.objects.get(id=self.params["account"]["order_id"])
        except Order.DoesNotExist:
            return

    def validate_order(self):
        if self.order.is_paid:
            self.error = True
            self.error_message = self.ORDER_ALREADY_PAID_MESSAGE
            self.code = self.ORDER_ALREADY_PAID

    def validate_amount(self, amount):
        if amount != self.order.transaction_amount:
            self.error = True
            self.error_message = self.INVALID_AMOUNT_MESSAGE
            self.code = self.INVALID_AMOUNT

    def cancel_transaction(self):
        try:
            transaction = Transaction.objects.get(transaction_id=self.params["id"], order__provider=Provider.PAYME)
        except Transaction.DoesNotExist:
            return True, self.TRANSACTION_NOT_FOUND_MESSAGE, self.TRANSACTION_NOT_FOUND

        if transaction.status != TransactionStatus.WAITING:
            return True, self.UNABLE_TO_PERFORM_OPERATION, self.UNABLE_TO_PERFORM_OPERATION_MESSAGE

        return self.error, self.error_message, self.code
