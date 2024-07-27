from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework import permissions


router = DefaultRouter()
router.register('book', BookViewSet, basename='BookViewSet')
router.register('character', CharacterViewSet, basename='CharacterViewSet')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:book_id>/posts/', AllPostByBookView.as_view(), name='book_posts'),
    path('my_posts/', AllPostByUserView.as_view(), name='user-posts'),
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='like'),
    path('posts/<int:pk>/liked_users/', PostViewSet.as_view({'get': 'liked_users'}), name='liked-users'),
    path('books/<int:book_id>/comments/', AllCommentsByBookView.as_view(), name='book-comments'),
    path('my_comments/', AllCommentsByUserView.as_view(), name='usercomments'),
    path('comments/<int:pk>/like/', CommentViewSet.as_view({'post': 'like'}), name='comment-like'),
    path('comments/<int:pk>/liked_users/', CommentViewSet.as_view({'get': 'liked_users'}), name='comment-liked-users'),
    path('<int:book_id>/characters/', BookCharactersAPIView.as_view(), name='book-characters'),
    path('AllBooks/', MainPageAllBooksAPIView.as_view(), name='main-page-all-books'),
    path('MyBooks/', MainPageMybooksAPIView.as_view(), name='main-page-my-books'),
    # ex) path('pages/<int:year>/', AllPagesView.as_view(), name='all-pages-list'),
]