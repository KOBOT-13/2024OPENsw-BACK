from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, permissions
from django.db.models import Q

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

class UserReadBookCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserBookCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserReadBooksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_books = UserBook.objects.filter(user=user).order_by('-read_date')
        serializer = UserBookSerializer(user_books, many=True)
        return Response(serializer.data)

class ToggleWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        user = request.user

        try:
            # Wishlist에서 해당 유저와 책을 찾음
            wishlist_item = Wishlist.objects.filter(user=user, book_id=book_id).first()

            if wishlist_item:
                # 존재하면 삭제 (찜 취소)
                wishlist_item.delete()
                return Response({"message": "찜 목록에서 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
            else:
                # 존재하지 않으면 추가
                Wishlist.objects.create(user=user, book_id=book_id)
                return Response({"message": "찜 목록에 추가되었습니다."}, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({"error": "책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class UserWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        wishlist_items = Wishlist.objects.filter(user=user).values_list('book_id', flat=True)
        return Response(list(wishlist_items))

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

class BookListByTagView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        tag_id = self.kwargs['tag_id']
        return Book.objects.filter(tags__id=tag_id)

class BookSearchView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        query = self.request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)