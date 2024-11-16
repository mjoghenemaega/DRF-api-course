# chat/views.py
from rest_framework import generics
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from django.contrib.auth import get_user_model

class ChatListView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(seeker=user) | Chat.objects.filter(provider=user)

    def perform_create(self, serializer):
        seeker = self.request.user
        provider_id = self.request.data.get('provider')
        provider = get_user_model().objects.get(id=provider_id)
        serializer.save(seeker=seeker, provider=provider)

class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

    def perform_create(self, serializer):
        chat = Chat.objects.get(id=self.kwargs['chat_id'])
        serializer.save(chat=chat, sender=self.request.user)

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        message_content = request.data.get('message')

        chat = Chat.objects.get(id=chat_id)
        message = Message.objects.create(
            chat=chat, sender=request.user, message=message_content
        )

        return Response({'status': 'Message sent successfully'})

class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can delete
    serializer_class = ChatSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        # Restrict deletion to the user involved in the chat
        user = self.request.user
        return Chat.objects.filter(seeker=user) | Chat.objects.filter(provider=user)


class MessageDeleteView(DestroyAPIView):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        # Restrict deletion to messages sent by the user
        user = self.request.user
        return Message.objects.filter(sender=user)
