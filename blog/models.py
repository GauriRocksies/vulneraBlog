"""
VulneraBlog Models
Defines all database models for the platform.
"""

import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


def generate_user_id():
    """Generate a unique VulneraBlog user ID like VLR_88920-X"""
    digits = ''.join(random.choices(string.digits, k=5))
    suffix = random.choice(string.ascii_uppercase)
    return f"VLR_{digits}-{suffix}"


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds VulneraBlog-specific fields.
    """
    user_id_code = models.CharField(
        max_length=15,
        unique=True,
        editable=False,
        help_text='Auto-generated VulneraBlog user identifier'
    )
    bio = models.TextField(blank=True, help_text='User biography')
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='Profile picture'
    )
    role = models.CharField(
        max_length=150,
        blank=True,
        help_text='e.g. Lead Curator & Designer'
    )
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate unique user_id_code on first save
        if not self.user_id_code:
            candidate = generate_user_id()
            while User.objects.filter(user_id_code=candidate).exists():
                candidate = generate_user_id()
            self.user_id_code = candidate
        super().save(*args, **kwargs)

    @property
    def followers_count(self):
        return Follow.objects.filter(following=self).count()

    @property
    def following_count(self):
        return Follow.objects.filter(follower=self).count()

    @property
    def display_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def __str__(self):
        return self.username


class Tag(models.Model):
    """Post tags like #BRUTALISM, #CURATION, etc."""
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):
    """
    Blog post model with support for categories, tags, likes,
    cover images, and read time estimation.
    """
    CATEGORY_CHOICES = [
        ('architecture', 'Architecture'),
        ('tech_noir', 'Tech Noir'),
        ('design', 'Design'),
        ('editorial', 'Editorial'),
        ('typography', 'Typography'),
        ('culture', 'Culture'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=300)
    content = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='editorial'
    )
    cover_image = models.ImageField(
        upload_to='post_covers/',
        blank=True,
        null=True
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_time = models.PositiveIntegerField(
        default=5,
        help_text='Estimated reading time in minutes'
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.filter(parent=None).count()

    @property
    def total_engagement(self):
        return self.likes_count + self.comments.count()

    def get_category_display_upper(self):
        return self.get_category_display().upper()

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Comment model with support for nested replies and likes.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User,
        related_name='liked_comments',
        blank=True
    )
    # Self-referential FK for nested replies
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    class Meta:
        ordering = ['created_at']

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return f"Comment by {self.author.username} on '{self.post.title}'"


class Follow(models.Model):
    """
    Represents a follow relationship between two users.
    """
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_set'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers_set'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"


class Bookmark(models.Model):
    """
    Saved/bookmarked posts per user.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='bookmarked_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked '{self.post.title}'"