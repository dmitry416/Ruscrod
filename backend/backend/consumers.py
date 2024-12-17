from channels.generic.websocket import AsyncWebsocketConsumer

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("group", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            await self.channel_layer.group_send("group", {"type": "text_message",
                                                          "data": text_data})
        elif bytes_data:
            await self.channel_layer.group_send("group", {"type": "audio_message",
                                                                "data": bytes_data})

    async def audio_message(self, event):
        data = event["data"]
        await self.send(bytes_data=data)

    async def text_message(self, event):
        data = event["data"]
        await self.send(text_data=data)
