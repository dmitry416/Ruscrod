from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.CharField(max_length=255)
    groups = models.ManyToManyField('auth.Group', related_name='api_user_set', blank=True,
                                    help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                    verbose_name='groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='api_user_set', blank=True,
                                              help_text='Specific permissions for this user.',
                                              verbose_name='user permissions')


class Server(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='server_images/', null=True, blank=True)
    owner = models.ForeignKey(User, related_name='owned_servers', on_delete=models.CASCADE)


class Room(models.Model):
    name = models.CharField(max_length=255)
    server = models.ForeignKey(Server, related_name='rooms', on_delete=models.CASCADE, null=True, blank=True)


class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friendships1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendships2', on_delete=models.CASCADE)
    is_friend = models.BooleanField(default=True)


class UserRoom(models.Model):
    user = models.ForeignKey(User, related_name='user_rooms', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room_users', on_delete=models.CASCADE)


class ServerMember(models.Model):
    server = models.ForeignKey(Server, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='servers', on_delete=models.CASCADE)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
