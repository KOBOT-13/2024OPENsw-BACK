from django.db import models
from .models import User, Book, Quiz, Conversation

class QuizRecord(models.Model):
    id = models.AutoField(primary_key=True) # 퀴즈 기록 ID, 고유 식별자
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 사용자 ID (참조: User 테이블)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE) # 퀴즈 ID (참조: Quiz 테이블)
    score = models.IntegerField() # 퀴즈 점수
    completed_at = models.DateTimeField()  # 퀴즈를 완료한 날짜와 시간

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title} - {self.score}'

class ConversationRecord(models.Model):
    id = models.AutoField(primary_key=True) # 퀴즈 기록 ID, 고유 식별자
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 사용자 ID (참조: User 테이블)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE) # 대화 ID (참조: Conversation 테이블)
    completed_at = models.DateTimeField()  # 대화를 완료한 날짜와 시간

    def __str__(self):
        return f'{self.user.username} - {self.conversation.topic}'

