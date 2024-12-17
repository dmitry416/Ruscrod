from rest_framework import serializers
from .models import User, Room, Server, Friendship, UserRoom, ServerMember, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'image']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'server']

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ['id', 'name', 'image', 'owner']

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['user1', 'user2', 'is_friend']

class UserRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoom
        fields = ['user', 'room']

class ServerMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerMember
        fields = ['server', 'user']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'message', 'timestamp']