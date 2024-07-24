from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('conversation', ConversationViewSet, basename='ConversationViewSet')
router.register('message', MessageViewSet, basename='MessageViewSet')


urlpatterns = [
    path('', include(router.urls)),
    # ex) path('pages/<int:year>/', AllPagesView.as_view(), name='all-pages-list'),
    path('user_message/', UserMessageView.as_view(), name='user_message'),
]