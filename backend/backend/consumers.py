from channels.generic.websocket import AsyncWebsocketConsumer
from api.models import Room, User, Message
import json
from asgiref.sync import sync_to_async


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room = await sync_to_async(Room.objects.get)(id=self.room_id)
        self.room_name = f"room_{self.room_id}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            await self.channel_layer.group_send(self.room_name, {"type": "audio_message",
                                                                 "data": bytes_data})
        else:
            text_data_json = json.loads(text_data)
            message_data = text_data_json.get("data")
            username = text_data_json.get("username")
            user = await sync_to_async(User.objects.get)(username=username)
            message = await sync_to_async(Message.objects.create)(
                room=self.room,
                user=user,
                message=message_data
            )

        await self.channel_layer.group_send(self.room_name, {"type": "text_message",
                                                                 "message": message_data,
                                                                 "username": username,
                                                                 "timestamp": message.timestamp.isoformat()})

    async def audio_message(self, event):
        data = event["data"]
        await self.send(bytes_data=data)

    async def text_message(self, event):
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]

        await self.send(text_data=json.dumps({
            "type": "text_message",
            "message": message,
            "username": username,
            "timestamp": timestamp
        }))
