"""
VulneraBlog Admin Configuration
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment, Tag, Follow, Bookmark


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'user_id_code', 'email', 'role', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'user_id_code', 'email', 'first_name', 'last_name')
    readonly_fields = ('user_id_code',)
    fieldsets = UserAdmin.fieldsets + (
        ('VulneraBlog Profile', {
            'fields': ('user_id_code', 'bio', 'avatar', 'role', 'location', 'website')
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'read_time', 'created_at', 'is_featured')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {}
    filter_horizontal = ('tags', 'likes')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'parent')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__title')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')