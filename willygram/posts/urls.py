from django.urls import path
from .views import (all_posts, create_post, feed, view_post, like_post, delete_post, 
    create_comment, delete_comment, explore)

urlpatterns = [
    path('posts/', all_posts, name='all-posts'),
    path('new/', create_post, name='post-create'),
    path('feed/', feed, name='feed'),
    path('post/<int:post_id>/', view_post, name='view-post'),
    path('like/', like_post, name='like-post'),
    path('delete/', delete_post, name='delete-post'),
    path('new_comment/', create_comment, name='create-comment'),
    path('delete_comment/', delete_comment, name='delete-comment'),
    path('explore/', explore, name='explore')
]