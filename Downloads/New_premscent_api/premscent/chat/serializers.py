# chat/serializers.py
from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'message', 'timestamp']

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = ['seeker', 'provider', 'messages', 'created_at']
