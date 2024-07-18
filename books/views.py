from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from .serializers import *
from django.conf import settings

# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class BookCharactersAPIView(generics.ListAPIView):
    serializer_class = CharacterSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Character.objects.filter(book_id=book_id)

class MainPageAllBooksAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class MainPageMybooksAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        my_books = user.mybook_list.all()
        serializer = MainPageBookSerializer(my_books, many=True)
        return Response(serializer.data)