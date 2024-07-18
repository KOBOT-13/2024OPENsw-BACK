from django.contrib import admin
from .models import QuizRecord, ConversationRecord

admin.site.register(QuizRecord)
admin.site.register(ConversationRecord)