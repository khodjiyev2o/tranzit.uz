from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.order.api_endpoints.List.serializers import OrderListSerializer
from apps.order.models import Order, Request


@receiver(post_save, sender=Order)
def order_updated(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    if created and instance.status == Order.OrderStatus.REQUESTED:
        # if new order is created
        data = {
            "type": "new_order",
            "data": OrderListSerializer(instance).data,
        }

        async_to_sync(channel_layer.group_send)("orders", {"type": "new_order", "data": data})
    elif instance.status == Order.OrderStatus.IN_PROGRESS or instance.status == Order.OrderStatus.CANCELED:
        # if order is taken by another driver
        data = {
            "type": "delete_order",
            "data": OrderListSerializer(instance).data,
        }
        async_to_sync(channel_layer.group_send)("orders", {"type": "delete_order", "data": data})
    elif instance.status == Order.OrderStatus.REQUESTED:
        data = {
            "type": "new_order",
            "data": OrderListSerializer(instance).data,
        }

        async_to_sync(channel_layer.group_send)("orders", {"type": "new_order", "data": data})


@receiver(post_delete, sender=Order)
def order_deleted(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    # if order is deleted fully
    data = {
        "type": "delete_order",
        "data": OrderListSerializer(instance).data,
    }
    async_to_sync(channel_layer.group_send)("orders", {"type": "delete_order", "data": data})


@receiver(post_save, sender=Request)
def request_created(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    print("Signal is working")
    if created:
        # if new requst is created
        data = {
            "type": "new_request_to_driver",
            "data": OrderListSerializer(instance.order).data,
        }
        async_to_sync(channel_layer.group_send)(
            f"driver_personal_group_{instance.driver.user.id}", {"type": "new_request", "data": data}
        )
