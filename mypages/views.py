from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import QuizRecord, ConversationRecord
from quizzes.models import Quiz
from django.utils import timezone

class QuizRecordViewSet(viewsets.ModelViewSet):
    queryset = QuizRecord.objects.all()
    serializer_class = QuizRecordSerializer

class ConversationRecordViewSet(viewsets.ModelViewSet):
    queryset = ConversationRecord.objects.all()
    serializer_class = ConversationRecordSerializer
class QuizRecordListView(generics.ListAPIView):
    serializer_class = QuizRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return QuizRecord.objects.filter(user=user).select_related('quiz').order_by('-completed_at')
