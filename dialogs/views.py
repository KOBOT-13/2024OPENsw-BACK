from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, viewsets, generics
from .serializers import *

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
