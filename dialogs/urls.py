from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('conversation', ConversationViewSet, basename='ConversationViewSet')
router.register('message', MessageViewSet, basename='MessageViewSet')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:conversation_id>/messages/', MessageAPIView.as_view(), name='conversation-messages'),
    # ex) path('pages/<int:year>/', AllPagesView.as_view(), name='all-pages-list'),

    path('mtt/', MessagetoTTS.as_view(), name='user_message'),
    path('endchat/', SummaryMessage.as_view(), name="end_chat"),
]
