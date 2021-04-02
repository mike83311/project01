from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token


import binascii
import os
from datetime import timedelta


DEFAULT_TOKEN_DURATION = 1


class User(AbstractUser):
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('Users')
        verbose_name_plural = _('Users')


class UserToken(models.Model):
    """
    A model refer from rest_framework.authtoken.models.Token,
    customized with token expiring mechanism.
    """
    key = models.CharField(_('Key'), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='user', db_column='user_id',
        on_delete=models.CASCADE, verbose_name=_('User')
    )
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    expires = models.DateTimeField(_('Expires in'))

    class Meta:
        db_table = 'user_token'
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')

    def save(self, *args, **kwargs):
        """
        Get default duration from 'EXPIRING_TOKEN_DURATION' in settings.py.
        If 'EXPIRING_TOKEN_DURATION' not found, set default duration as 1 hour.
        """
        if not self.pk:  # on create
            self.key = self.generate_key()
            self.refresh_expires()

        # Execute original save().
        return super().save(*args, **kwargs)

    def is_expired(self):
        """
        Check if token is expired.
        """
        return self.expires - timezone.now() < timedelta(seconds=0)

    def refresh_expires(self, duration=None):
        if duration is None:
            try:
                duration = settings.DEFAULT_TOKEN_DURATION
            except AttributeError:
                duration = DEFAULT_TOKEN_DURATION

        self.expires = timezone.now() + timedelta(hours=duration)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class ApiKey(models.Model):
    key = models.CharField(_('Key'), max_length=100, unique=True)
    group = models.OneToOneField(
        Group, related_name='group', on_delete=models.CASCADE, verbose_name=_('Group'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    class Meta:
        db_table = 'api_key'

    def save(self, *args, **kwargs):
        """
        Generate key on create.
        """
        if not self.pk:  # on create
            self.key = self.generate_key()

        # Execute original save().
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
