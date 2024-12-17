from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoomViewSet, ServerViewSet, YandexAuthView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'servers', ServerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth', YandexAuthView.as_view(), name='yandex_auth'),
]

'''
Пример использования ;)

GET:
/api/users/get_friends
/api/rooms/get_rooms
/api/rooms/1/get_room_messages/?page=1
/api/rooms/1/get_room_members
/api/servers/get_servers
/api/servers/1/get_server_rooms
/api/servers/{server_id}/get_server_members

POST:
/api/users/add_friend  (для полноценной дружбы нужно, чтобы этот запрос отправили оба. пока так)
{
    "name": "friend_username"
}

/api/users/delete_friend
{
    "name": "friend_username"
}

/api/rooms/create_room
{
    "name": "New Room",
    "friend_name": "friend_username"
}

/api/rooms/1/add_friend_to_room
{
    "friend_name": "friend_username"
}

/api/servers/create_server
{
    "name": "New Server",
    "image": "server_images/new_server.png"
}

/api/servers/1/set_server_image
{
    "image": "server_images/updated_image.png"
}

/api/servers/1/create_server_room
{
    "name": "New Room"
}

/api/servers/1/delete_server_room
'''