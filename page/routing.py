from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/speech_to_text/$', consumers.SpeechToTextConsumer.as_asgi()),
]
