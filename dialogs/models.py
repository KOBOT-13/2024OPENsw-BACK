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
