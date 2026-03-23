"""
Custom Django template tags and filters for VulneraBlog.
"""

from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.filter
def time_ago(value):
    """Convert a datetime to a human-readable relative time string."""
    if not value:
        return ''
    now = timezone.now()
    diff = now - value

    if diff < timedelta(minutes=1):
        return 'just now'
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f'{minutes}m ago'
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f'{hours}h ago'
    elif diff < timedelta(days=7):
        days = diff.days
        return f'{days}d ago'
    else:
        return value.strftime('%b %d, %Y').upper()


@register.filter
def format_count(value):
    """Format large numbers: 1200 → 1.2k"""
    try:
        value = int(value)
        if value >= 1000:
            return f'{value / 1000:.1f}k'
        return str(value)
    except (TypeError, ValueError):
        return value


@register.simple_tag
def post_liked(post, user):
    """Check if a user has liked a post."""
    return user in post.likes.all()