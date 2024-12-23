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
        friends = User.objects.filter(
            Q(friendships1__user2=user, friendships1__is_friend=True) |
            Q(friendships2__user1=user, friendships2__is_friend=True)
        ).distinct()
        serializer = UserSerializer(friends, many=True)
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
        members = room.room_users.all().values_list('user', flat=True)
        users = User.objects.filter(id__in=members)
        serializer = UserSerializer(users, many=True)
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
            return Response({"error": "Друг не найден"}, status=status.HTTP_200_OK)
        if UserRoom.objects.filter(user=friend, room=room).exists():
            return Response({"error": "Друг уже находится в этой комнате"}, status=status.HTTP_200_OK)
        UserRoom.objects.create(user=friend, room=room)
        return Response({"success": "Друг был добавлен"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    @permission_classes([IsAuthenticated])
    def leave_from_room(self, request, pk=None):
        room = self.get_object()
        user = request.user
        try:
            user_room = UserRoom.objects.get(user=user, room=room)
            user_room.delete()
            return Response({"success": "Вы успешно покинули комнату"}, status=status.HTTP_200_OK)
        except UserRoom.DoesNotExist:
            return Response({"warning": "Вы не состоите в этой комнате"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    @permission_classes([IsAuthenticated])
    def change_room_name(self, request, pk=None):
        room = self.get_object()
        new_name = request.data.get('name')
        if not new_name:
            return Response({"error": "Название не может быть пустым"}, status=status.HTTP_200_OK)
        room.name = new_name
        room.save()
        return Response({"success": "Название комнаты успешно изменено"}, status=status.HTTP_200_OK)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    @action(detail=False, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_servers(self, request):
        user = request.user
        servers = Server.objects.filter(members__user=user).select_related('owner')
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
        serializer = ServerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        name = validated_data.get('name')
        image = validated_data.get('image')
        server = Server.objects.create(name=name, image=image, owner=request.user)
        ServerMember.objects.create(server=server, user=request.user)
        serializer = ServerSerializer(server)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    @permission_classes([IsAuthenticated])
    def set_server_image(self, request, pk=None):
        server = self.get_object()
        if server.owner != request.user:
            return Response({"error": "You are not the owner of this server"}, status=status.HTTP_403_FORBIDDEN)
        image = request.data.get('image')
        server.image = image
        server.save()
        serializer = ServerSerializer(server, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        server = self.get_object()
        if server.owner != request.user:
            return Response({"error": "You are not the owner of this server"}, status=status.HTTP_403_FORBIDDEN)
        room_id = request.data.get('room_id')
        if not room_id:
            return Response({"error": "Room_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            room = Room.objects.get(id=room_id, server_id=server.id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
        room.delete()
        return Response({"message": "Room deleted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    @permission_classes([IsAuthenticated])
    def rename_server_room(self, request, pk=None):
        server = self.get_object()
        if server.owner != request.user:
            return Response({"error": "You are not the owner of this server"}, status=status.HTTP_403_FORBIDDEN)
        new_name = request.data.get('name')
        room_id = request.data.get('room_id')
        if not new_name or not room_id:
            return Response({"error": "Name and room_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            room = Room.objects.get(id=room_id, server_id=server.id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
        room.name = new_name
        room.save()
        return Response({"message": "Room renamed"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_server_members(self, request, pk=None):
        server = self.get_object()
        members = server.members.all().values_list('user', flat=True)
        users = User.objects.filter(id__in=members)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    @permission_classes([IsAuthenticated])
    def leave_from_server(self, request, pk=None):
        server = self.get_object()
        user = request.user

        if server.owner == user:
            return Response({"error": "Вы являетесь владельцем сервера и не можете его покинуть"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            user_server = ServerMember.objects.get(user=user, server=server)
            user_server.delete()
            return Response({"success": "Вы успешно покинули сервер"}, status=status.HTTP_200_OK)
        except ServerMember.DoesNotExist:
            return Response({"error": "Вы не состоите в этом сервере"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    @permission_classes([IsAuthenticated])
    def delete_server(self, request, pk=None):
        server = self.get_object()
        user = request.user

        if server.owner != user:
            return Response({"error": "Вы не являетесь владельцем сервера и не можете его удалить"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            server.delete()
            return Response({"success": "Сервер успешно удален"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['patch'])
    @permission_classes([IsAuthenticated])
    def update_server(self, request, pk=None):
        server = self.get_object()
        user = request.user

        if server.owner != user:
            return Response({"error": "Вы не являетесь владельцем сервера и не можете его изменить"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ServerSerializer(server, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    @permission_classes([IsAuthenticated])
    def join_server(self, request):
        server_name = request.data.get('name')
        if not server_name:
            return Response({"error": "Имя сервера не указано"}, status=status.HTTP_200_OK)
        server = Server.objects.filter(name=server_name).first()
        if not server:
            return Response({"error": "Сервер с таким именем не найден"}, status=status.HTTP_200_OK)
        if ServerMember.objects.filter(server=server, user=request.user).exists():
            return Response({"warning": "Вы уже являетесь участником этого сервера"}, status=status.HTTP_200_OK)
        ServerMember.objects.create(server=server, user=request.user)
        return Response({"success": "Вы успешно присоединились к серверу"}, status=status.HTTP_200_OK)
