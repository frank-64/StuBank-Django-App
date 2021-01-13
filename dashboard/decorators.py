from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.models import Helper


def valid_helper(function=None):
    def is_helper(u):
        if login_required and not u.is_authenticated:
            return False
        return Helper.objects.filter(user=u).exists()
    actual_decorator = user_passes_test(is_helper)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator
