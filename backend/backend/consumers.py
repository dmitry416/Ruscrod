from channels.generic.websocket import AsyncWebsocketConsumer

class AudioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("audio_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("audio_group", self.channel_name)
        print("Пидорасик съебался")

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            await self.channel_layer.group_send("audio_group", {"type": "audio_message",
                                                                "data": bytes_data})

    async def audio_message(self, event):
        data = event["data"]
        await self.send(bytes_data=data)
