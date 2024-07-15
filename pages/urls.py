from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pages.views import PageViewSet

router = DefaultRouter()
# DefaultRouter는 RESTful API의 라우팅을 자동으로 처리해주는 편리한 도구입니다
# ex) router.register('pages', PageViewSet, basename = 'PageViewSet')
router.register('page', PageViewSet, basename='PageViewSet')

urlpatterns = [
    path('', include(router.urls)),
    # ex) path('pages/<int:year>/', AllPagesView.as_view(), name='all-pages-list'),


]