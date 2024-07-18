from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *

class QuizRecordViewSet(viewsets.ModelViewSet):
    queryset = QuizRecord.objects.all()
    serializer_class = QuizRecordSerializer

class ConversationRecordViewSet(viewsets.ModelViewSet):
    queryset = ConversationRecord.objects.all()
    serializer_class = ConversationRecordSerializer