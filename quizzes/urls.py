from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('book_id_quizzes/<int:book_id>/', AllQuizzesByBookView.as_view(), name='book-quizzes'),
]