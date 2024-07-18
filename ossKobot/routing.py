from django.urls import path
from pages import consumers

websocket_urlpatterns = [
    path('ws/speech-to-text/', consumers.SpeechToTextConsumer.as_asgi()),
]