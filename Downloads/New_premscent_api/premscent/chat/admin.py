from django.contrib import admin
from .models import Chat, Message

# Registering the Chat model
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'seeker', 'provider', 'created_at')  # Use fields from Chat model
    search_fields = ('seeker__username', 'provider__username')  # Search by usernames of seeker and provider
    list_filter = ('created_at',)  # Add filters for easy navigation
    ordering = ('-created_at',)  # Default ordering by creation time

# Registering the Message model
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'message', 'timestamp')  # Use 'message' field instead of 'content'
    search_fields = ('message', 'sender__username')  # Search by message content or sender's username
    list_filter = ('timestamp', 'chat')  # Filters for timestamp and chat
    ordering = ('-timestamp',)  # Default ordering by timestamp
