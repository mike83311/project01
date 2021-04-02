from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import Group

from .models import UserToken


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Return user.
        Return nothing if login failed.
        """
        # Execute default auth backend.
        user = super().authenticate(request, username, password, **kwargs)

        if user is None:  # login failed
            return
        # elif not 'gemtek' in user.groups.values_list('name', flat=True) or user.is_superuser != 1:
        #     # Restrict users not in 'gemtek' group or not superuser from login.
        #     return
        # elif 'app' in user.username:  # Restrict 'app' user from login.
        #     return
        else:  # login success
            # Remove old tokens.
            delete_tokens(user)
            # Create new token.
            try:
                UserToken.objects.create(user=user)
                return user
            except:  # Cannot create token, login failed.
                return


def delete_tokens(user):
    """
    Remove tokens if exist.
    """
    try:
        token_query_results = UserToken.objects.filter(user=user.id)
        if token_query_results.exists():
            token_query_results.delete()
    except:
        return


def do_after_logout(sender, user, request, **kwargs):
    """
    Delete tokens after user logout.
    """
    if user is not None:
        delete_tokens(user)


user_logged_out.connect(do_after_logout)
