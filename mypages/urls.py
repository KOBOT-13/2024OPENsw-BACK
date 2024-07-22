from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('quizRecord', QuizRecordViewSet, basename='QuizRecordViewSet')

urlpatterns = [
    path('', include(router.urls)),
    path('quiz_record', QuizRecordListView.as_view(), name='quiz-record-list'),
    path('quiz/<int:quiz_id>/record/', SaveQuizRecordView.as_view(), name = 'save-quiz-record'),

]