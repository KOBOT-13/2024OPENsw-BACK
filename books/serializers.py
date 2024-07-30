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

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'book', 'post_date', 'update_date', 'likes_count', 'likes', 'body']

    def get_likes_count(self, obj):
        return obj.likes.count()

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
