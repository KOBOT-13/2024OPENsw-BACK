from django.db import models
from django.conf import settings



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

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.AutoField(primary_key=True) # 게시글 ID
    body = models.TextField(max_length=3000) # 게시글 내용 (3000자 이내)
    likes = models.PositiveIntegerField(default=0) # 좋아요 수
    post_date = models.DateTimeField(auto_now_add=True) # 게시글 발행일자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 사용자 ID (참조: users 테이블)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # 책 ID (참조: books 테이블)
