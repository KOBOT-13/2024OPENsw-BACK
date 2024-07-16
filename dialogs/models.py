from django.db import models
from django.contrib.auth.models import User  # Assuming you are using Django's built-in User model
from books.models import Book, Character

class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)  # 대화 ID
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자 ID (참조: users 테이블)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)  # 책 ID (참조: books 테이블)
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)  # 등장인물 ID (참조: character 테이블)
    created_at = models.DateTimeField(auto_now_add=True)  # 대화 시작 시간
    updated_at = models.DateTimeField(auto_now=True)  # 마지막 대화 시간


    def __str__(self):
        return f"Conversation between {self.user.username} and {self.character.name} in {self.book.title}"
class Message(models.Model):
    SENDER_TYPE_CHOICES = [
        ('user', 'User'),
        ('character', 'Character')
    ]

    message_id = models.AutoField(primary_key=True)  # 메시지 ID
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)  # 대화 ID (참조: conversations 테이블)
    sender_type = models.CharField(max_length=10, choices=SENDER_TYPE_CHOICES)  # 보낸 사람의 타입 (User 또는 Character)
    user_sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # 사용자 ID (참조: users 테이블)
    character_sender = models.ForeignKey(Character, null=True, blank=True, on_delete=models.CASCADE)  # 등장인물 ID (참조: character 테이블)
    message = models.TextField()  # 대화 내용
    timestamp = models.DateTimeField(auto_now_add=True)  # 대화가 발생한 시간

    def clean(self):
        if self.sender_type == 'user' and not self.user_sender:
            raise ValueError("sender_type is 'user', but user_sender is not set.")
        if self.sender_type == 'character' and not self.character_sender:
            raise ValueError("sender_type is 'character', but character_sender is not set.")
        if self.sender_type == 'user' and self.character_sender:
            raise ValueError("sender_type is 'user', but character_sender is set.")
        if self.sender_type == 'character' and self.user_sender:
            raise ValueError("sender_type is 'character', but user_sender is set.")

    def save(self, *args, **kwargs):
        self.clean()  # Perform the clean method to check validity before saving
        super().save(*args, **kwargs)

    def __str__(self):
        sender = self.user_sender if self.sender_type == 'user' else self.character_sender
        return f"Message from {sender} at {self.timestamp}"