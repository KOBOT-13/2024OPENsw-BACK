from django.db import models
from django.conf import settings  

class QuizRecord(models.Model):
    id = models.AutoField(primary_key=True) # 퀴즈 기록 ID, 고유 식별자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 사용자 ID (참조: User 테이블)
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE) # 퀴즈 ID (참조: Quiz 테이블)
    score = models.IntegerField() # 퀴즈 점수
    completed_at = models.DateTimeField()  # 퀴즈를 완료한 날짜와 시간
    book_title = models.CharField(max_length=200) # 책 제목
    book_cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True) # 책 표지 이미지

    def __str__(self):
        return f'{self.user.username} - {self.quiz} - {self.score}'

