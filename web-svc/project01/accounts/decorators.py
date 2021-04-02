from django.contrib.auth.decorators import user_passes_test

from .models import UserToken


def token_expire_checked(function=None):
    def check_token(uid):
        try:
            token = UserToken.objects.get(user=uid)
        except UserToken.DoesNotExist:
            return False

        if token is None:
            return False
        elif token.is_expired():
            token.delete()
            return False
        else:
            token.refresh_expires()
            token.save()
            return True

    actual_decorator = user_passes_test(check_token)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator
