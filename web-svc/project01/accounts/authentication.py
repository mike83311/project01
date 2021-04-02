from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from .models import UserToken, ApiKey


class CustomTokenAuthentication(BaseAuthentication):
    """
    Overwrite to examine 'api_key' and 'api_secret' from request body.
    And check if token is expired.
    """
    keyword_key = 'api_key'
    keyword_secret = 'api_secret'
    model_key = ApiKey
    model_secret = UserToken

    def authenticate(self, request):
        # Check request method.
        if request.method != 'POST':  # Raise 405 Error.
            raise exceptions.MethodNotAllowed(request.method)

        # Retrieve 'key'
        if self.keyword_key in request.POST:
            key = request.POST.get(self.keyword_key)
        else:  # Raise 403 Error.
            raise exceptions.AuthenticationFailed(
                _(f'Missing authentication token: {self.keyword_key}.'))

        # Retrieve 'secret'
        if self.keyword_secret in request.POST:
            secret = request.POST.get(self.keyword_secret)
        else:    # Raise 403 Error.
            raise exceptions.AuthenticationFailed(
                _(f'Missing authentication token: {self.keyword_secret}.'))

        return self.authenticate_credentials(key, secret)

    def authenticate_credentials(self, key, secret):
        # Examine 'key'.
        try:
            _key = self.model_key.objects.get(key=key)
            _group = _key.group
        except self.model_key.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                f'Invalid {self.keyword_key}.')

        # Examine 'secret'.
        try:
            _secret = self.model_secret.objects.get(key=secret)
            _user = _secret.user
        except self.model_secret.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                f'Invalid {self.keyword_secret}.')

        # Check if user is inactivate.
        if not _user.is_active:
            raise exceptions.PermissionDenied(
                f'Your {self.keyword_secret} is inactive.')

        # Check if token is expired.
        if _secret.is_expired():
            raise exceptions.PermissionDenied(
                f'Your {self.keyword_secret} has expired.')

        # Check if the user is in the group.
        if _group not in _user.groups.all():
            raise exceptions.AuthenticationFailed(
                f'Invalid {self.keyword_key} or {self.keyword_secret}.')

        return _user, _secret
