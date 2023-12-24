from functools import wraps

from django.shortcuts import render


def specialist_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_specialist):
            render(request, 'accounts/403.html', status=403)
        return view_func(request, *args, **kwargs)

    return _wrapped_view