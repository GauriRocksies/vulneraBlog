"""
Custom authentication backend for VulneraBlog.
Allows users to log in using their generated user_id_code (e.g. VLR_88920-X)
instead of a username.
"""

from django.contrib.auth.backends import BaseBackend
from .models import User


class UserIDBackend(BaseBackend):
    """
    Authenticates against User.user_id_code + password.
    """

    def authenticate(self, request, user_id_code=None, password=None, **kwargs):
        if user_id_code is None or password is None:
            return None
        try:
            user = User.objects.get(user_id_code=user_id_code)
        except User.DoesNotExist:
            # Run the default password hasher to reduce timing attack risk
            User().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_pk):
        try:
            return User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return None