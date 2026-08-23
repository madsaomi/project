from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import Http404


def role_required(role):
    """
    Декоратор: проверяет, что пользователь залогинен И имеет нужную роль.
    Если роль не совпадает — поднимает Http404 (чтобы не раскрывать наличие эндпоинта).
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if getattr(request.user, 'role', None) != role:
                raise Http404
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def student_required(view_func):
    """Только для зарегистрированных студентов."""
    return role_required('student')(view_func)


def employer_required(view_func):
    """Только для зарегистрированных работодателей."""
    return role_required('employer')(view_func)
