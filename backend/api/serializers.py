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
    owner_username = serializers.CharField(source='user.username', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Server
        fields = ['id', 'name', 'image', 'owner_username']

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)

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