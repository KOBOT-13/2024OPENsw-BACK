from django.utils import timezone
from rest_framework import serializers
from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = '__all__'

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
        fields = ['id', 'title', 'cover_image', 'tags']


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
        fields = ['book', 'read_date']

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
