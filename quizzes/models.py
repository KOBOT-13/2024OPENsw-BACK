from django.db import models
from books.models import Book

class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True) # id

    book_id = models.ForeignKey(Book, related_name='quizz', on_delete=models.CASCADE)  # 책과의 관계
    title = models.CharField(max_length=200)  # 퀴즈 제목
    quiz_image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)  # 퀴즈 이미지

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz_id = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)  # 퀴즈와의 관계

    question_text = models.TextField()  # 질문 텍스트
    correct_answer = models.IntegerField()  # 정답 (선지번호)
    option_one = models.CharField(max_length=200)  # 선택지 1
    option_two = models.CharField(max_length=200)  # 선택지 2
    option_three = models.CharField(max_length=200, blank=True)  # 선택지 3
    option_four = models.CharField(max_length=200, blank=True)  # 선택지 4
    question_image = models.ImageField(upload_to='question_images/', blank=True, null=True)  # 질문 이미지

    def __str__(self):
        return self.question_text


