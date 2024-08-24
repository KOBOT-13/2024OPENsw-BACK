from django.db import models
from ossKobot import settings

CATEGORY_CHOICE = {
    ('fantasy', '판타지'),
    ('novel', '소설'),
    ('picture book', '그림책'),
    ('biography', '위인전'),
    ('traditional fairy tale', '전래동화'),
    ('fable', '우화'),
}


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 태그 이름

    def __str__(self):
        return self.name


class Book(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200, blank=True, null=True)  # 출판사
    publication_date = models.DateField(blank=True, null=True)  # 출판 일자
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)  # 책 사진
    synopsis = models.TextField(blank=True)  # 줄거리
    category = models.CharField(verbose_name='카테고리', choices=CATEGORY_CHOICE, blank=True, null=True)  # 카테고리
    tags = models.ManyToManyField(Tag, related_name='books', blank=True)  # 태그
    wish_count = models.IntegerField(default=0)  # 이 책을 좋아요 한 유저의 수

    def __str__(self):
        return self.title


class WrittenBook(models.Model): # 내가 쓴 책
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reder_writtenBook', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField(blank=True, null=True)  # 출판 일자
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)  # 책 사진
    synopsis = models.TextField(blank=True)  # 줄거리
    summary_story = models.TextField(blank=True)
    category = models.CharField(verbose_name='카테고리', choices=CATEGORY_CHOICE, blank=True, null=True)  # 카테고리
    tags = models.ManyToManyField(Tag, related_name='written_books', blank=True)  # 태그


class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    character_image = models.ImageField(upload_to='character_image/', blank=True, null=True)
    greeting = models.CharField(max_length=200)  # 인사말
    book = models.ForeignKey(Book, related_name='book', on_delete=models.CASCADE, null=True)  # 책과의 관계
    writtenbook = models.ForeignKey(WrittenBook, related_name='writtenbook', on_delete=models.CASCADE, null=True)
    
    # 상세 설정
    speaker = models.CharField(max_length=100, null=True)
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


class Post(models.Model):  # 독후감
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='post', on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)  # 발행 일자
    update_date = models.DateTimeField(auto_now=True)  # 수정 일자
    body = models.TextField(max_length=3000)  # 내용 (3000자 이내)

    def __str__(self):
        return f'comment by {self.user.username} on {self.book.title}'


class Comment(models.Model):  # 나의 생각 공유
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)    # 내용 (500자 이내)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_likes', blank=True)  # 좋아요 한 유저들

    def __str__(self):
        return f'Comment by {self.user.username} on {self.book.title}'


class BookRequest(models.Model):  # 책 추가 요청
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    character = models.CharField(max_length=100, blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 요청한 유저

    def __str__(self):
        return self.title


class UserBook(models.Model):  # 내가 읽은 책
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reader_thisbook', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='books_readByUser', on_delete=models.CASCADE)
    read_date = models.DateField()  # 이 책을 읽은 날짜
    weight = models.FloatField(default=0.5)  # 선호도

    class Meta:
        unique_together = ('user', 'book')
        # 내가 이 책을 읽었다는 정보는 한 쌍만 저장됨.
        # read_date 는 읽을 때 마다 갱신

    def __str__(self):
        return f'{self.user.username} - {self.book.title} read {self.read_date}'


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reader_wishThisbook', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='books_wishlisted', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        # 내가 이 책을 찜했다는 정보는 한 쌍만 저장됨.

    def __str__(self):
        return f'{self.user.username} - {self.book.title} press wish at {self.added_at}'


class RecommendBooks(models.Model):  # 추천 도서
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reader_recommendBook', on_delete=models.CASCADE)
    recommended_books = models.JSONField()

    def __str__(self):
        return f'Recommend {self.user.username}'
