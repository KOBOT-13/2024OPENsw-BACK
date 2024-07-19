from django.contrib import admin
from .models import Conversation, Message, AudioText, TTSRequest

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(AudioText)

@admin.register(TTSRequest)
class TTSRequestAdmin(admin.ModelAdmin):
    list_display = ('text', 'speaker', 'volume', 'speed', 'pitch', 'created_at', 'tts_file')