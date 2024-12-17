from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .consumers import RoomConsumer

websocket_urlpatterns = [
    path('ws/room', RoomConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})