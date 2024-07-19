from django.db import models
from books.models import Book

class Quiz(models.Model):
    id = models.AutoField(primary_key=True) # 퀴즈 ID

    quiz_text = models.TextField()  # 질문 텍스트
    answer = models.IntegerField()  # 정답 (선지번호)
    option_one = models.CharField(max_length=200)  # 선택지 1
    option_two = models.CharField(max_length=200)  # 선택지 2
    option_three = models.CharField(max_length=200, blank=True)  # 선택지 3
    option_four = models.CharField(max_length=200, blank=True)  # 선택지 4
    quiz_image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)  # 질문 이미지

    def __str__(self):
        return self.quiz_text


