from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import QuizRecord
from quizzes.models import Quiz
from django.utils import timezone

class QuizRecordViewSet(viewsets.ModelViewSet):
    queryset = QuizRecord.objects.all()
    serializer_class = QuizRecordSerializer

class QuizRecordListView(generics.ListAPIView):
    serializer_class = QuizRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return QuizRecord.objects.filter(user=user).select_related('quiz').order_by('-completed_at')

class SaveQuizRecordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        user = request.user
        # quiz = Quiz.objects.get(id=quiz_id)
        book = request.book
        score = request.data.get('score')
        completed_at = timezone.now() # 현재 시간
        
        quiz_record = QuizRecord.objects.create(
            user=user,
            # quiz=quiz,
            score=score,
            completed_at=completed_at,
            book_title=book.title,
            book_cover_image=book.cover_image
        )
        
        return Response({'message': 'Quiz record saved successfully'}, status=status.HTTP_201_CREATED)
