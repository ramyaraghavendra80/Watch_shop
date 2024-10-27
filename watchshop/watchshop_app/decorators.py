from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def admin_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_superuser or user.groups.filter(
            name='Admin').exists(),
        login_url='home'  # You can redirect unauthorized users to the home page or another URL
    )(view_func)
    return decorated_view_func
