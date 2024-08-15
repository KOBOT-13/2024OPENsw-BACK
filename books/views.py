import pandas as pd
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, permissions
from django.db.models import Q
from datetime import datetime

from .models import *
from .recommned_utils import *
from .serializers import *
from django.conf import settings

from .emotion_analysis import *

# Create your views here.
books = pd.read_csv('books/recommend/fairytale_data - Sheet1 (3).csv')
content_similarity = compute_content_similarity(books)

def get_user_age(self, birth_date):
    """생년월일을 이용해 나이를 계산하는 함수"""
    print(birth_date)
    if birth_date is None:
        return None
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

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

class BookRecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_age(self, birth_date):
        """생년월일을 이용해 나이를 계산하는 함수"""
        print(birth_date)
        if birth_date is None:
            return None
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def get(self, request):

        # 1. 미리 계산된 책 데이터와 유사도 사용
        global books, content_similarity  # 전역 변수로 미리 로드된 데이터 사용

        # 2. 사용자의 읽은 책 목록과 호감도(weight) 가져오기
        user_books = UserBook.objects.filter(user=request.user)

        if not user_books.exists():
            return Response({"error": "사용자가 읽은 책 목록이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        print(request.user.birth_date)

        # 3. user_data 생성
        user_titles = []
        user_ratings = []
        user_age = self.get_user_age(request.user.birth_date)

        if user_age is None:
            return Response({"error": "생년월일 정보가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        for user_book in user_books:
            user_titles.append(user_book.book.title)
            user_ratings.append(user_book.weight)

        user_data = pd.DataFrame({
            'user_id': [request.user.id] * len(user_titles),
            'age': [user_age] * len(user_titles),
            'title': user_titles,
            'rating': user_ratings
        })

        # 4. 사용자 유사도 계산 (이 부분은 요청마다 다를 수 있음)
        user_similarity = compute_user_similarity(user_data, books)

        # 5. 추천 시스템 실행
        recommended_books = hybrid_recommendation(user_titles, user_ratings, books, content_similarity, user_similarity)

        # 6. 추천된 책의 제목을 기반으로 Book 모델에서 ID 조회
        recommended_titles = recommended_books['title'].tolist()
        recommended_ids = list(Book.objects.filter(title__in=recommended_titles).values_list('id', flat=True))

        # 7. 기존 추천 결과 삭제
        RecommendBooks.objects.filter(user=request.user).delete()

        # 8. 추천 결과를 RecommendBooks에 저장
        RecommendBooks.objects.create(user=request.user, recommended_books=recommended_ids)

        # 9. 추천된 책의 ID 리스트 반환
        return Response({"recommended_book_ids": list(recommended_ids)}, status=status.HTTP_200_OK)


class RecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            recommendation = RecommendBooks.objects.filter(user=request.user).first()
            return Response({"recommended_book_ids": recommendation.recommended_books}, status=status.HTTP_200_OK)
        except RecommendBooks.DoesNotExist:
            return Response({"error": "추천 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class UserReadBookCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserBookCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
[]
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
        user = self.request.user
        book_id = serializer.data.get('book')
        post = serializer.data.get('body')
        print(post)
        analysis = emotion_analysis(post)
        print(analysis)
        book_post = get_object_or_404(UserBook, user=user, book=book_id)
        book_post.weight = analysis
        book_post.save()

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

