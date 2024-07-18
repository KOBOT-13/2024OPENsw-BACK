from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

router = DefaultRouter()
# DefaultRouter는 RESTful API의 라우팅을 자동으로 처리해주는 편리한 도구입니다
# ex) router.register('pages', PageViewSet, basename = 'PageViewSet')


urlpatterns = [
    path('', views.home, name='home'),
    # ex) path('pages/<int:year>/', AllPagesView.as_view(), name='all-pages-list'),
    path('audiotext/', AudioTextView.as_view(), name='audio-txt'),


]