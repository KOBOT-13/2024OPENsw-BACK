from django.db import models

class Book(models.Model):
    id = models.AutoField(primary_key=True) # id

    title = models.CharField(max_length=200)  # 책 제목
    author = models.CharField(max_length=100)  # 저자
    publisher = models.CharField(max_length=200, blank=True, null=True) # 출판사
    publication_date = models.DateField(blank=True, null=True) # 출판일자
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)  # 책 사진
    synopsis = models.TextField(blank=True)  # 줄거리
    content = models.TextField(blank=True) # 책 내용

    created_at = models.DateTimeField(auto_now_add=True) # 책 추가 날짜
    updated_at = models.DateTimeField(auto_now=True) # 책 수정 날짜

    def __str__(self):
        return self.title

class Character(models.Model):
    id = models.AutoField(primary_key=True) # id
    name = models.CharField(max_length=100)  # 등장인물 이름
    description = models.TextField(blank=True)  # 등장인물 설명
    character_image = models.ImageField(upload_to='character_image/', blank=True, null=True)  # 등장인물 사진
    book_id = models.ForeignKey(Book, related_name='characters', on_delete=models.CASCADE)  # 책과의 관계

    def __str__(self):
        return self.name

class Quiz(models.Model):
    book = models.ForeignKey(Book, related_name='quizz', on_delete=models.CASCADE)  # 책과의 관계
    title = models.CharField(max_length=200)  # 퀴즈 제목

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)  # 퀴즈와의 관계
    question_text = models.TextField()  # 질문 텍스트
    correct_answer = models.IntegerField()  # 정답 (선지번호)
    option_one = models.CharField(max_length=200)  # 선택지 1
    option_two = models.CharField(max_length=200)  # 선택지 2
    option_three = models.CharField(max_length=200, blank=True)  # 선택지 3
    option_four = models.CharField(max_length=200, blank=True)  # 선택지 4

    def __str__(self):
        return self.question_text

