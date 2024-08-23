from django.utils import timezone
from rest_framework import serializers
from .models import *

CATEGORY_CHOICE = {
    ('fantasy', '판타지'),
    ('novel', '소설'),
    ('picture book', '그림책'),
    ('biography', '위인전'),
    ('traditional fairy tale', '전래동화'),
    ('fable', '우화'),
}


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        
    def to_representation(self, instance):
        # 데이터를 클라이언트로 반환할 때 호출됨
        ret = super().to_representation(instance)
        # 카테고리 필드를 한글로 변환하여 반환
        ret['category'] = dict(CATEGORY_CHOICE).get(instance.category, instance.category)
        return ret

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        book = Book.objects.create(**validated_data)
        book.tags.set(tag_ids)
        return book

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        instance = super().update(instance, validated_data)
        instance.tags.set(tag_ids)
        return instance


class MainPageBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'cover_image', 'tags', 'category']


class UserBookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields = ['book']

    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data['book']
        read_date = timezone.now()  # 현재 시간을 사용하여 read_date 설정
        print(read_date)

        # 동일한 책이 이미 존재하는 경우 업데이트
        user_book_instance, created = UserBook.objects.update_or_create(
            user=user,
            book=book,
            defaults={'read_date': read_date}
        )
        print(user_book_instance)

        return user_book_instance


class UserBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()  # 책 제목을 반환하기 위해 BookSerializer 사용
    # read_date = serializers.SerializerMethodField()

    class Meta:
        model = UserBook
        fields = ['book', 'read_date', 'weight']

    # def get_read_date(self, obj):
    #     # read_date를 날짜 형식으로 반환
    #     return obj.read_date.strftime('%Y-%m-%d')


class WishlistSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(source='book.id')

    class Meta:
        model = Wishlist
        fields = ['book_id']


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'user', 'book', 'post_date', 'update_date', 'body']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'book', 'created_at', 'updated_at', 'likes_count', 'likes', 'content']

    def get_likes_count(self, obj):
        return obj.likes.count()

class BookRequestSerializer(serializers.ModelSerializer):
    requested_by = serializers.ReadOnlyField(source='requested_by.username')

    class Meta:
        model = BookRequest
        fields = '__all__'

class WrittenBookSerializer(serializers.ModelSerializer):
    character = serializers.ListField(child=serializers.CharField(),required=False)
    speaker = serializers.ListField(child=serializers.CharField(),required=False)
    class Meta:
        model = WrittenBook
        fields = ['id', 'user', 'title', 'author', 'publication_date', 'cover_image', 'synopsis', 'summary_story', 'character', 'speaker', 'category', 'tags']

    def validate(self, data):
        # author 필드를 user의 username으로 설정
        if not data.get('author'):
            data['author'] = self.context['request'].user.username
        
        # publication_date가 설정되지 않은 경우, 오늘 날짜로 설정
        if not data.get('publication_date'):
            data['publication_date'] = timezone.now().date()

        return data
    
    def create(self, validated_data):
        # character와 speaker는 모델에 저장되지 않으므로 제거
        character = validated_data.pop('character', None)
        speaker = validated_data.pop('speaker', None)
        
        tags = validated_data.pop('tags', [])

        # 나머지 데이터로 WrittenBook 인스턴스 생성
        written_book = WrittenBook.objects.create(**validated_data)
        
        written_book.tags.set(tags)

        # character와 speaker를 활용한 추가 로직 (저장, 로그, 알림 등)을 여기에 추가 가능

        return written_book