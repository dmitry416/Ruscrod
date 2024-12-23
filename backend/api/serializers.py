import re

from rest_framework import serializers

from .models import User, Room, Server, Friendship, UserRoom, ServerMember, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'image']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'server']

class ServerSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Server
        fields = ['id', 'name', 'image', 'owner_username']

    def validate_name(self, value):
        if not (3 <= len(value) <= 30):
            raise serializers.ValidationError("Название сервера должно быть от 3 до 30 символов.")

        if Server.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Сервер с таким названием уже существует.")

        return value

    def update(self, instance, validated_data):
        if 'image' not in validated_data:
            validated_data['image'] = instance.image

        return super().update(instance, validated_data)

class FriendshipSerializer(serializers.ModelSerializer):
    user1_username = serializers.CharField(source='user1.username', read_only=True)
    user2_username = serializers.CharField(source='user2.username', read_only=True)

    class Meta:
        model = Friendship
        fields = ['user1_username', 'user2_username', 'is_friend']

class UserRoomSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserRoom
        fields = ['username', 'room']

class ServerMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ServerMember
        fields = ['server', 'username']

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'username', 'message', 'timestamp']