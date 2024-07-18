from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from .serializers import *

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

