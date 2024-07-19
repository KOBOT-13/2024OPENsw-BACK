from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('quizRecord', QuizRecordViewSet, basename='QuizRecordViewSet')
router.register('conversationRecord', ConversationRecordViewSet, basename='ConversationRecordViewSet')

urlpatterns = [
    path('', include(router.urls)),
    # ex) path('pages/<int:year>/', AllPagesView.as_view(), name='all-pages-list'),

    path('quiz_record', QuizRecordListView.as_view(), name='quiz-record-list'),
    path('quiz/<int:quiz_id>/record/', SaveQuizRecordView.as_view(), name = 'save-quiz-record'),

]