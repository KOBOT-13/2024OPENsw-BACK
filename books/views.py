from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, permissions

from .models import *
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
    permission_classes = [AllowAny]
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

class PostViewSet(viewsets.ModelViewSet): # 독후감에 대한 CRUD
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllPostByBookView(ListAPIView): # 특정 책에 대한 모든 독후감
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Post.objects.filter(book_id=book_id).order_by('-post_date')

class AllPostByUserView(ListAPIView): # 특정 유저에 대한 모든 독후감
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            return Response({'status': 'comment unliked'})
        else:
            comment.likes.add(user)
            return Response({'status': 'comment liked'})

    @action(detail=True, methods=['get'])
    def liked_users(self, request, pk=None):
        comment = self.get_object()
        liked_users = comment.likes.all()
        liked_users_data = [{'id': user.id, 'username': user.username} for user in liked_users]
        return Response({'liked_users': liked_users_data})

class AllCommentsByBookView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Comment.objects.filter(book_id=book_id).order_by('-created_at')

class AllCommentsByUserView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(user=user)

class BookRequestViewSet(viewsets.ModelViewSet):
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)