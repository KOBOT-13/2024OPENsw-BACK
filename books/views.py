from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from django.db.models import Q
from datetime import datetime
from .recommned_utils import *
from .serializers import *
from .emotion_analysis import *
from .models import *
import json
import socket
from .myBook import *

# 추천 시스템 초기 세팅
books = pd.read_csv('books/recommend/fairytale_data - Sheet1 (3).csv')  # 책 데이터
content_similarity = compute_content_similarity(books)  # 책 유사도


class BookViewSet(viewsets.ModelViewSet):  # Book model CRUD
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CharacterViewSet(viewsets.ModelViewSet):  # Character model CRUD
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class BookCharactersAPIView(generics.ListAPIView):  # Book ID에 해당하는 캐릭터 GET
    serializer_class = CharacterSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Character.objects.filter(book_id=book_id)


class MainPageAllBooksAPIView(APIView):  # 메인 페이지에서, 모든 책 Object GET
    permission_classes = [AllowAny]  # 메인 페이지는 인증 없이 접속 가능

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
class WrittenBookAPIView(APIView):
    queryset = WrittenBook.objects.all()
    serializer_class = WrittenBookSerializer


class BookRecommendationAPIView(APIView):  # 추천 책 생성 API
    permission_classes = [IsAuthenticated]

    def get_user_age(self, birth_date):  # 나이 계산 함수
        if birth_date is None:
            return None
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def get(self, request):
        # 1. 미리 계산된 책 데이터와 유사도 사용
        # 전역 변수로 미리 로드된 데이터 사용
        global books, content_similarity

        # 2. 사용자의 읽은 책 목록과 선호도 가져오기
        user_books = UserBook.objects.filter(user=request.user)
        if not user_books.exists():
            return Response({"error": "사용자가 읽은 책 목록이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

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

        # 4. 사용자 유사도 계산
        user_similarity = compute_user_similarity(user_data, books)

        # 5. 추천 시스템 실행
        recommended_books = hybrid_recommendation(user_titles, user_ratings, books, content_similarity, user_similarity)

        # 6. 추천된 책의 제목을 기반으로 Book 모델에서 ID 조회
        recommended_titles = recommended_books['title'].tolist()
        recommended_ids = list(Book.objects.filter(title__in=recommended_titles).values_list('id', flat=True))
        recommended_objects = Book.objects.filter(title__in=recommended_titles)
        serializer = BookSerializer(recommended_objects, many=True)

        # 7. 기존 추천 결과 삭제
        RecommendBooks.objects.filter(user=request.user).delete()

        # 8. 추천 결과를 RecommendBooks 에 저장
        RecommendBooks.objects.create(user=request.user, recommended_books=recommended_ids)

        # 9. 추천된 책들의 정보 반환
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecommendationAPIView(APIView):  # 추천 책 결과 GET
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recommendation = RecommendBooks.objects.filter(user=request.user).first()

        # recommendation 이 None 일 경우 처리
        if not recommendation:
            return Response({"error": "추천 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        book_ids = recommendation.recommended_books
        book_objects = Book.objects.filter(id__in=book_ids)
        serializer = BookSerializer(book_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserReadBookCreateAPIView(APIView):  # 내가 읽은 책에 추가
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserBookCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReadBooksAPIView(APIView):  # 내가 읽은 책 목록 GET
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_books = UserBook.objects.filter(user=user).order_by('-read_date')
        serializer = UserBookSerializer(user_books, many=True)
        return Response(serializer.data)


class ToggleWishlistAPIView(APIView):  # 유저별 찜 목록에 추가/삭제  # 책별 찜 카운트 증가/감소
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        user = request.user

        try:
            wishlist_item = Wishlist.objects.filter(user=user, book_id=book_id).first()
            book = Book.objects.filter(id=book_id).first()

            if wishlist_item:
                wishlist_item.delete()
                book.wish_count -= 1
                book.save()
                return Response({"message": "찜 목록에서 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
            else:
                Wishlist.objects.create(user=user, book_id=book_id)
                book.wish_count += 1
                book.save()
                return Response({"message": "찜 목록에 추가되었습니다."}, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({"error": "책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)


class UserWishlistAPIView(APIView):  # 유저의 찜 목록 GET
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        wishlist_items = Wishlist.objects.filter(user=user)
        books = [item.book for item in wishlist_items]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):  # Post model CRUD
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):  # Post Create 시 감정 분석  # 감정 분석 후 선호도 저장
        serializer.save(user=self.request.user)
        user = self.request.user
        book_id = serializer.data.get('book')
        post = serializer.data.get('body')
        analysis = emotion_analysis(post)
        book_post = get_object_or_404(UserBook, user=user, book=book_id)
        book_post.weight = analysis
        book_post.save()


class AllPostByBookView(ListAPIView):  # 해당 책에 대한 모든 독후감 GET
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Post.objects.filter(book_id=book_id).order_by('-post_date')


class AllPostByUserView(ListAPIView):  # 해당 유저의 모든 독후감 GET
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user)


class CommentViewSet(viewsets.ModelViewSet):  # Comment model CRUD
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])  # Comment 에 대한 부가 기능 1
    def like(self, request, pk=None):  # Comment 좋아요/취소
        comment = self.get_object()
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            return Response({'status': 'comment unliked'})
        else:
            comment.likes.add(user)
            return Response({'status': 'comment liked'})

    @action(detail=True, methods=['get'])  # Comment 에 대한 부가 기능 2
    def liked_users(self, request, pk=None):  # Comment 를 좋아요 한 유저 GET
        comment = self.get_object()
        liked_users = comment.likes.all()
        liked_users_data = [{'id': user.id, 'username': user.username} for user in liked_users]
        return Response({'liked_users': liked_users_data})


class AllCommentsByBookView(ListAPIView):  # 특정 책에 대한 모든 Comment GET
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Comment.objects.filter(book_id=book_id).order_by('-created_at')


class AllCommentsByUserView(ListAPIView):  # 유저가 작성한 모든 Comment GET
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


class WrittenBookViewSet(viewsets.ModelViewSet):  # WrittenBook model CRUD
    queryset = WrittenBook.objects.all()
    serializer_class = WrittenBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 로그인한 사용자가 작성한 책만 반환
        return WrittenBook.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        title = data.get('title')
        synopsis = data.get('synopsis')
        character = data.get('character', [])
        speaker = data.get('speaker', [])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        writtenbook = serializer.save()
        
        for i in range(len(character)):
            if speaker[i] == "여자_어린아이": speaker = "nyejin"
            elif speaker[i] == "남자_어린아이": speaker = "njonghyun"
            elif speaker[i] == "여자_성인": speaker = "dara-danna"
            elif speaker[i] == "남자_성인": speaker = "ndonghyun"
            elif speaker[i] == "여자_노인": speaker = "nsunhee"
            elif speaker[i] == "남자_노인": speaker = "nsunhee"
            char_request = Character.objects.create(
                name = character[i],
                description = f"{character[i]}에 대한 설명입니다.",
                greeting = f"안녕하세요, 저는 {character[i]}입니다.",
                writtenbook = writtenbook,
                speaker = speaker,
                character_image='profile_image.png'
            )
            char_request.save()
            
        summary_story = story_analyze(title, character, synopsis) # 원하는 함수명으로 변경
        
        writtenbook.summary_story = summary_story
        
        tag, category = make_tag(title, synopsis)
        writtenbook.category = category
        
        writtenbook.save()
        
        tag_objects = Tag.objects.filter(name__in=tag)
        writtenbook.tags.set(tag_objects)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)    


class AudioFileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, filename):
        if not filename.endswith('.mp3'):
            filename += '.mp3'
        
        file_path = os.path.join(settings.MEDIA_ROOT, 'audio', filename)

        if os.path.exists(file_path):
            file_url = f"{settings.MEDIA_URL}audio/{filename}"
            return Response({"file_url": file_url}, status=200)
        else:
            raise Http404("File does not exist")


class WrittenBookCharactersAPIView(generics.ListAPIView):  # WrittenBook ID에 해당하는 캐릭터 GET
    serializer_class = CharacterSerializer

    def get_queryset(self):
        writtenbook_id = self.kwargs['writtenbook_id']
        return Character.objects.filter(writtenbook_id=writtenbook_id)