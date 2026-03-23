"""
VulneraBlog URL patterns
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    #path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Main pages
    path('', views.home_view, name='home'),
    path('explore/', views.explore_view, name='explore'),
    path('bookmarks/', views.bookmarks_view, name='bookmarks'),

    # Posts
    path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('post/upload/', views.upload_post_view, name='upload_post'),
    path('post/<int:pk>/edit/', views.edit_post_view, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post_view, name='delete_post'),

    # AJAX toggles
    path('post/<int:pk>/like/', views.like_post_view, name='like_post'),
    path('post/<int:pk>/bookmark/', views.bookmark_post_view, name='bookmark_post'),
    path('comment/<int:pk>/like/', views.like_comment_view, name='like_comment'),

    # Profile
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/me/', views.edit_profile_view, name='edit_profile'),
    path('user/<str:username>/follow/', views.follow_user_view, name='follow_user'),
]