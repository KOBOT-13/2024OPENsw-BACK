from django.db import models
from django.conf import settings  

class QuizRecord(models.Model):
    id = models.AutoField(primary_key=True) # 퀴즈 기록 ID, 고유 식별자
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 사용자 ID (참조: User 테이블)
    score = models.IntegerField() # 퀴즈 점수
    completed_at = models.DateTimeField(auto_now_add=True)  # 퀴즈를 완료한 날짜와 시간


    def __str__(self):
        return f'{self.user.username} - {self.book} - {self.score}'