from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework import permissions


router = DefaultRouter()
router.register('book', BookViewSet, basename='BookViewSet')
router.register('character', CharacterViewSet, basename='CharacterViewSet')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:book_id>/characters/', BookCharactersAPIView.as_view(), name='book-characters'),
    path('AllBooks/', MainPageAllBooksAPIView.as_view(), name='main-page-all-books'),
    path('MyBooks/', MainPageMybooksAPIView.as_view(), name='main-page-my-books'),
    # ex) path('pages/<int:year>/', AllPagesView.as_view(), name='all-pages-list'),
]