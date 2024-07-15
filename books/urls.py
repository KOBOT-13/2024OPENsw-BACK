from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework import permissions


router = DefaultRouter()
router.register('book', BookViewSet, basename='BookViewSet')
router.register('character', CharacterViewSet, basename='CharacterViewSet')

urlpatterns = [
    path('', include(router.urls)),
    # ex) path('pages/<int:year>/', AllPagesView.as_view(), name='all-pages-list'),
]