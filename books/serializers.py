from rest_framework import serializers
from .models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class MainPageBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'cover_image']


class UserBookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields = ['book', 'read_date']

    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data['book']
        read_date = validated_data['read_date']

        user_book, created = UserBook.objects.update_or_create(
            user=user,
            book=book,
            defaults={'read_date': read_date}
        )

        return user_book


class UserBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()  # 책 제목을 반환하기 위해 StringRelatedField 사용

    class Meta:
        model = UserBook
        fields = ['book', 'read_date']

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
