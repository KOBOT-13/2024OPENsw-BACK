from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

router = DefaultRouter()


urlpatterns = [
    path('', views.home, name='home'),
    path('audiotext/', AudioTextView.as_view(), name='audio-txt'),


]