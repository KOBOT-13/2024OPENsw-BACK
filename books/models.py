from django.db import models
from django.conf import settings

from ossKobot import settings


class Book(models.Model):
    id = models.AutoField(primary_key=True) # id
    title = models.CharField(max_length=200)  # 책 제목
    author = models.CharField(max_length=100)  # 저자
    publisher = models.CharField(max_length=200, blank=True, null=True) # 출판사
    publication_date = models.DateField(blank=True, null=True) # 출판일자
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)  # 책 사진
    synopsis = models.TextField(blank=True)  # 줄거리

    def __str__(self):
        return self.title


class Character(models.Model):
    id = models.AutoField(primary_key=True) # id
    name = models.CharField(max_length=100)  # 등장인물 이름
    description = models.TextField(blank=True)  # 등장인물 설명
    character_image = models.ImageField(upload_to='character_image/', blank=True, null=True)  # 등장인물 사진
    greeting = models.CharField(max_length=200) # 등장인물 인사말
    book = models.ForeignKey(Book, related_name='characters', on_delete=models.CASCADE)  # 책과의 관계

    speaker = models.CharField(max_length=100)
    volume = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    pitch = models.IntegerField(default=0)
    emotion = models.IntegerField(default=0)
    emotion_strength = models.IntegerField(default=0)
    format = models.CharField(max_length=10, default="mp3")
    alpha = models.IntegerField(default=0)
    end_pitch = models.IntegerField(default=0)
        
    def __str__(self):
        return self.name


# 독후감과 나의생각공유는 코드가 동일합니다. 디비만 달라요
class Post(models.Model): # '독후감'
    id = models.AutoField(primary_key=True) # 게시글 ID
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post', on_delete=models.CASCADE)  # 사용자 ID (참조: AUTH_USER_MODEL(CustomUser) 테이블)
    book = models.ForeignKey(Book, related_name='post', on_delete=models.CASCADE)  # 책 ID (참조: books 테이블)
    post_date = models.DateTimeField(auto_now_add=True) # 게시글 발행일자
    update_date = models.DateTimeField(auto_now=True) # 게시글 수정일자
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_like', blank=True) # 좋아요 수
    body = models.TextField(max_length=3000)  # 게시글 내용 (3000자 이내)

    def __str__(self):
        return f'comment by {self.user.username} on {self.book.title}'

class Comment(models.Model): # '나의 생각 공유'
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)  # 짧은 코멘트 내용 (500자 이내)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_likes', blank=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.book.title}'

class BookRequest(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    character = models.CharField(max_length=100, blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
