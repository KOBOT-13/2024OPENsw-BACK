from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('quiz', QuizViewSet, basename= 'QuizViewSet')
router.register('question', QuesitonViewSet, basename='QuestionViewSet')

urlpatterns = [
    path('', include(router.urls)),
    # ex) path('pages/<int:year>/', AllPagesView.as_view(), name='all-pages-list'),
]
