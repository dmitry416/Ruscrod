from django.contrib import admin
from .models import User, Server, Room, Friendship, UserRoom, ServerMember, Message

admin.site.register(User)
admin.site.register(Server)
admin.site.register(Room)
admin.site.register(Friendship)
admin.site.register(UserRoom)
admin.site.register(ServerMember)
admin.site.register(Message)