from django.contrib import admin
from .models import QuizRecord, ConversationRecord

class QuizRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quiz', 'score', 'completed_at')
    
admin.site.register(QuizRecord)
admin.site.register(ConversationRecord)