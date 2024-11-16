from django.urls import path
from .views import (
    ChatListView,
    MessageListView,
    SendMessageView,
    ChatDeleteView,  # New import
    MessageDeleteView  # New import
)
app_name = 'chat'

urlpatterns = [
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('chats/<int:chat_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('chats/<int:chat_id>/messages/send/', SendMessageView.as_view(), name='send-message'),
    path('chats/<int:pk>/delete/', ChatDeleteView.as_view(), name='chat-delete'),  # Delete chat
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message-delete'),  # Delete message
]
