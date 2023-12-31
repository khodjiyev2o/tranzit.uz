import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):
    driver_group_name = "orders"

    async def connect(self):
        user = self.scope["user"]
        self.driver_personal_group = f"driver_personal_group_{user.id}"
        await self.accept()
        if user == AnonymousUser():
            """If token is expired or not provided"""
            await self.close(code=4001)

        await self.channel_layer.group_add(self.driver_personal_group, self.channel_name)
        await self.channel_layer.group_add(self.driver_group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.driver_group_name, self.channel_name)

    async def receive(self, text_data):
        print("text_data", text_data)

    async def new_order(self, event):
        """
        Send new order updates to the connected drivers in the 'orders' group
        """
        data = event["data"]
        await self.send(text_data=json.dumps(data))

    async def delete_order(self, event):
        """
        Send deleted order deletes to the connected drivers in the 'orders' group
        """
        data = event["data"]
        await self.send(text_data=json.dumps(data))

    async def new_request(self, event):
        """
        Send new order client request to the connected driver in the 'driver_personal_group_' group
        """
        data = event["data"]
        await self.send(text_data=json.dumps(data))
