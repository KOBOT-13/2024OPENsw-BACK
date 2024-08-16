from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework import permissions


router = DefaultRouter()
router.register('book', BookViewSet, basename='BookViewSet')
router.register('character', CharacterViewSet, basename='CharacterViewSet')
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')
router.register('book_requests', BookRequestViewSet, basename='book_request')


urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:book_id>/posts/', AllPostByBookView.as_view(), name='book-posts'),
    path('my_posts/', AllPostByUserView.as_view(), name='user-posts'),
    path('books/<int:book_id>/comments/', AllCommentsByBookView.as_view(), name='book-comments'),
    path('search/', BookSearchView.as_view(), name='book-search'),
    path('tag/<int:tag_id>/', BookListByTagView.as_view(), name='books_by_tag'),
    path('my_comments/', AllCommentsByUserView.as_view(), name='user-comments'),
    path('comments/<int:pk>/like/', CommentViewSet.as_view({'post': 'like'}), name='comment-like'),
    path('comments/<int:pk>/liked_users/', CommentViewSet.as_view({'get': 'liked_users'}), name='comment-liked-users'),
    path('<int:book_id>/characters/', BookCharactersAPIView.as_view(), name='book-characters'),
    path('AllBooks/', MainPageAllBooksAPIView.as_view(), name='main-page-all-books'),
    path('user-read-book-list/add/', UserReadBookCreateAPIView.as_view(), name='user-read-book-create'),
    path('user-read-book-list/get/', UserReadBooksAPIView.as_view(), name='user-read-books'),
    path('wishlist/toggle/<int:book_id>/', ToggleWishlistAPIView.as_view(), name='toggle-wishlist'),
    path('wishlist/', UserWishlistAPIView.as_view(), name='user-wishlist'),
    path('recommend/', BookRecommendationAPIView.as_view(), name='book-recommendation'),
    path('recommend/list/', RecommendationAPIView.as_view(), name='last-recommendation'),
]