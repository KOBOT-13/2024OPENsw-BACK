from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Quiz
from .serializers import *

class AllQuizzesByBookView(ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Quiz.objects.filter(book_id=book_id).order_by('id')

