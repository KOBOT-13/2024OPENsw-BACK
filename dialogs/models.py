from django.db import models
from django.conf import settings
from books.models import Book, Character, WrittenBook

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)  # 대화 ID
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 사용자 ID (참조: users 테이블)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)  # 책 ID (참조: books 테이블)
    written_book = models.ForeignKey(WrittenBook, on_delete=models.CASCADE, null=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)  # 등장인물 ID (참조: character 테이블)
    created_at = models.DateTimeField(auto_now_add=True)  # 대화 시작 시간
    updated_at = models.DateTimeField(auto_now=True)  # 마지막 대화 시간


    def __str__(self):
        if self.book is None:
            return f"Conversation between {self.user.username} and {self.character.name} in {self.written_book.title}"
        else:
            return f"Conversation between {self.user.username} and {self.character.name} in {self.book.title}"
    
    def has_messages(self):
        return self.messages.exists()

class Message(models.Model):
    SENDER_TYPE_CHOICES = [
        ('user', 'User'),
        ('character', 'Character')
    ]

    id = models.AutoField(primary_key=True)  # 메시지 ID
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)  # 대화 ID (참조: conversations 테이블)
    sender_type = models.CharField(max_length=10, choices=SENDER_TYPE_CHOICES)  # 보낸 사람의 타입 (User 또는 Character)
    user_sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)  # 사용자 ID (참조: users 테이블)
    character_sender = models.ForeignKey(Character, null=True, blank=True, on_delete=models.CASCADE)  # 등장인물 ID (참조: character 테이블)
    message = models.TextField()  # 대화 내용
    timestamp = models.DateTimeField(auto_now_add=True)  # 대화가 발생한 시간
    tts_file = models.FileField(upload_to='tts/', null=True, blank=True)

    def __str__(self):
        sender = self.user_sender if self.sender_type == 'user' else self.character_sender
        return f"Message from {sender} at {self.timestamp}"
    
class SummaryMessage(models.Model):
    id = models.AutoField(primary_key=True)
    user_sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    character_sender = models.ForeignKey(Character, null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField(default=0)
    end_key = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"SummaryMessage {self.user_sender} and {self.character_sender}"