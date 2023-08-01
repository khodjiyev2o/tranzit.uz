import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):
    driver_group_name = "orders"

    async def connect(self):
        user = self.scope["user"]
        await self.accept()
        if user == AnonymousUser():
            """If token is expired or not provided"""
            await self.close(code=4001)

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
        Send deleted order updates to the connected drivers in the 'orders' group
        """
        data = event["data"]
        await self.send(text_data=json.dumps(data))
