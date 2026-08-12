from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class RoleRequiredMixin(LoginRequiredMixin):
    """
    Mixin для Class-Based Views (CBV): проверяет, что залогиненный пользователь имеет нужную роль.
    """
    required_role = None  # Должен быть переопределен в наследнике: 'student' или 'employer'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.required_role and getattr(request.user, 'role', None) != self.required_role:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class StudentRequiredMixin(RoleRequiredMixin):
    """Mixin для запрета доступа всем, кроме студентов."""
    required_role = 'student'


class EmployerRequiredMixin(RoleRequiredMixin):
    """Mixin для запрета доступа всем, кроме работодателей."""
    required_role = 'employer'
