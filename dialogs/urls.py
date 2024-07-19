from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register('conversation', ConversationViewSet, basename='ConversationViewSet')
router.register('message', MessageViewSet, basename='MessageViewSet')


urlpatterns = [
    path('', include(router.urls)),
    # path('transcribe_audio/', views.transcribe_audio, name='transcribe_audio'),

    # ex) path('pages/<int:year>/', AllPagesView.as_view(), name='all-pages-list'),
    path('audiotext/', AudioTextView.as_view(), name='audio-txt'),
    path('tts/', tts, name='tts'),
    path('tts/file/<int:tts_request_id>/', get_tts_file, name='get_tts_file'),
    path('tts/file/', list_tts_files, name='list_tts_files'),

]