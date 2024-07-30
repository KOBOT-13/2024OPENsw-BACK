from django.db import models
from books.models import Book

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)  # 퀴즈 ID
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    question = models.TextField()  # 질문 텍스트
    options = models.JSONField()  # 옵션 필드 (JSON 형태, 리스트)
    answer = models.CharField(max_length=200)  # 정답 (텍스트)

    def __str__(self):
        return self.quiz_text





