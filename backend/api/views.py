from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import User, Room, Server, Friendship, UserRoom, ServerMember
from .serializers import UserSerializer, RoomSerializer, ServerSerializer, FriendshipSerializer, \
    ServerMemberSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated


class YandexAuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        login_data = request.data.get('login')
        image_url = request.data.get('image_url')

        user, created = User.objects.get_or_create(username=login_data)

        if created:
            user.username = login_data
        user.image = image_url
        user.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_friends(self, request):
        user = request.user
        friends = user.friendships1.filter(is_friend=True) | user.friendships2.filter(is_friend=True)
        serializer = FriendshipSerializer(friends, many=True)
        return Response(serializer.data)


    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=['post'])
    def add_friend(self, request):
        friend_name = request.data.get('name')
        friend = User.objects.filter(username=friend_name).first()
        if not friend:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_200_OK)
        if friend.username == request.user.username:
            return Response({"error": "С самим собой дружить нельзя!"}, status=status.HTTP_200_OK)

        existing_friendship = Friendship.objects.filter(
            (Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user))).first()

        if existing_friendship:
            if existing_friendship.is_friend:
                return Response({"warning": "Пользователь уже у вас в друзьях"}, status=status.HTTP_200_OK)
            else:
                if existing_friendship.user1.username == request.user.username:
                    return Response({"warning": "Запрос в друзья уже был отправлен"}, status=status.HTTP_200_OK)
                existing_friendship.is_friend = True
                existing_friendship.save()
                return Response({"success": "Запрос в друзья принят"}, status=status.HTTP_200_OK)

        Friendship.objects.create(user1=request.user, user2=friend, is_friend=False)

        return Response({"success": "Запрос в друзья был отправлен"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    @permission_classes([IsAuthenticated])
    def delete_friend(self, request):
        friend_name = request.data.get('name')
        friend = User.objects.filter(username=friend_name).first()
        if not friend:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_200_OK)

        Friendship.objects.filter(
            Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user)).delete()

        return Response({"success": "Вы бросили своего друга"}, status=status.HTTP_200_OK)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_rooms(self, request):
        user = request.user
        rooms = Room.objects.filter(room_users__user=user, server__isnull=True)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_room_messages(self, request, pk=None):
        room = self.get_object()
        page = int(request.query_params.get('page', 1))
        messages = room.messages.order_by('-timestamp')[(page - 1) * 50:page * 50]
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_room_members(self, request, pk=None):
        room = self.get_object()
        members = room.room_users.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    @permission_classes([IsAuthenticated])
    def create_room(self, request):
        name = request.data.get('name')
        room = Room.objects.create(name=name)
        UserRoom.objects.create(user=request.user, room=room)
        return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    @permission_classes([IsAuthenticated])
    def add_friend_to_room(self, request, pk=None):
        room = self.get_object()
        friend_name = request.data.get('friend_name')
        friend = User.objects.filter(username=friend_name).first()
        if not friend:
            return Response({"error": "Friend not found"}, status=status.HTTP_404_NOT_FOUND)
        UserRoom.objects.create(user=friend, room=room)
        return Response({"message": "Friend added to room"}, status=status.HTTP_201_CREATED)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    @action(detail=False, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_servers(self, request):
        user = request.user
        servers = Server.objects.filter(members__user=user)
        serializer = ServerSerializer(servers, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_server_rooms(self, request, pk=None):
        server = self.get_object()
        rooms = Room.objects.filter(server=server)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    @permission_classes([IsAuthenticated])
    def create_server(self, request):
        name = request.data.get('name')
        image = request.FILES.get('image')
        server = Server.objects.create(name=name, image=image, owner=request.user)
        ServerMember.objects.create(server=server, user=request.user)
        return Response(ServerSerializer(server).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    @permission_classes([IsAuthenticated])
    def set_server_image(self, request, pk=None):
        server = self.get_object()
        if server.owner != request.user:
            return Response({"error": "You are not the owner of this server"}, status=status.HTTP_403_FORBIDDEN)
        image = request.data.get('image')
        server.image = image
        server.save()
        return Response(ServerSerializer(server).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    @permission_classes([IsAuthenticated])
    def create_server_room(self, request, pk=None):
        server = self.get_object()
        if server.owner != request.user:
            return Response({"error": "You are not the owner of this server"}, status=status.HTTP_403_FORBIDDEN)
        name = request.data.get('name')
        room = Room.objects.create(name=name, server=server)
        return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    @permission_classes([IsAuthenticated])
    def delete_server_room(self, request, pk=None):
        room = self.get_object()
        if room.server.owner != request.user:
            return Response({"error": "You are not the owner of this server"}, status=status.HTTP_403_FORBIDDEN)
        room.delete()
        return Response({"message": "Room deleted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_server_members(self, request, pk=None):
        server = self.get_object()
        members = server.members.all()
        serializer = ServerMemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)