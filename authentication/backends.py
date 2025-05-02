from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:
            # Try to authenticate with email
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            # Try to authenticate with username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None
