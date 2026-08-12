---
name: security_and_auth
description: Правила безопасности, декораторы и пермиссии для доступа к представлениям.
---

# Безопасность и Доступ (Security & Auth)

## 1. Модель ролей

Проект использует кастомные роли через `User.Role` (TextChoices):
```python
class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Студент'
        EMPLOYER = 'employer', 'Работодатель'
        ADMIN = 'admin', 'Администратор'
```

Роль задаётся при регистрации и **не меняется** пользователем.

---

## 2. Готовые декораторы для проверки ролей

> ✅ Декораторы **реализованы** в `apps/accounts/decorators.py` (тесты в `apps/accounts/tests.py`).

```python
# apps/accounts/decorators.py

from functools import wraps
from django.http import Http404
from django.contrib.auth.decorators import login_required


def role_required(role):
    """
    Декоратор: проверяет, что пользователь залогинен И имеет нужную роль.
    Использование: @role_required('employer')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.role != role:
                raise Http404  # Не показываем 403, чтобы не раскрывать существование страницы
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def student_required(view_func):
    """Только для студентов."""
    return role_required('student')(view_func)


def employer_required(view_func):
    """Только для работодателей."""
    return role_required('employer')(view_func)
```

### Примеры использования:

```python
# views.py
from apps.accounts.decorators import student_required, employer_required

@student_required
def apply_for_internship(request, slug):
    """Только студент может откликнуться."""
    ...

@employer_required
def create_internship(request):
    """Только работодатель может создать стажировку."""
    ...

@employer_required
def dashboard(request):
    """Kanban-доска — только для работодателя."""
    ...
```

---

## 3. Object-level Permissions (защита объектов)

Недостаточно проверить роль — нужно проверить, что пользователь обращается **к своему** объекту.

### Паттерн: проверка владельца

```python
@employer_required
def edit_internship(request, slug):
    internship = get_object_or_404(Internship, slug=slug)

    # ⚠️ ОБЯЗАТЕЛЬНО: проверить что стажировка принадлежит этому работодателю
    if internship.company.user != request.user:
        raise Http404

    # ... логика редактирования
```

### Типичные проверки:

| Действие | Проверка |
|---|---|
| Студент редактирует свой профиль | `profile.user == request.user` |
| Работодатель смотрит свои отклики | `InternshipParticipant.objects.filter(internship__company__user=request.user)` |
| Работодатель редактирует свою стажировку | `internship.company.user == request.user` |
| Работодатель меняет статус кандидата | `participant.internship.company.user == request.user` |

### Mixin для CBV (Class-Based Views):

```python
# apps/accounts/mixins.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class RoleRequiredMixin(LoginRequiredMixin):
    """Mixin для CBV: проверяет роль пользователя."""
    required_role = None  # Задать в наследнике: 'student' или 'employer'

    def dispatch(self, request, *args, **kwargs):
        if self.required_role and request.user.role != self.required_role:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class StudentRequiredMixin(RoleRequiredMixin):
    required_role = 'student'


class EmployerRequiredMixin(RoleRequiredMixin):
    required_role = 'employer'
```

---

## 4. CSRF & XSS

### CSRF для обычных форм:
```html
<form method="POST">
    {% csrf_token %}
    <!-- поля формы -->
</form>
```

### CSRF для HTMX (настроено в base.html):
```html
<meta name="csrf-token" content="{{ csrf_token }}">
<script>
  document.body.addEventListener('htmx:configRequest', (e) => {
    e.detail.headers['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]').content;
  });
</script>
```

### XSS-защита:
- Django экранирует HTML по умолчанию.
- **НЕ используй** `{{ value|safe }}` — это XSS-уязвимость.
- Единственное исключение: контент, сгенерированный самим Django (обработанный Markdown и т.п.).

---

## 5. Чеклист безопасности для нового view

При создании **каждого** view проверь:

- [ ] `@login_required` или `@student_required`/`@employer_required`?
- [ ] Проверка владельца объекта (object-level permission)?
- [ ] POST-форма содержит `{% csrf_token %}`?
- [ ] HTMX POST отправляет `X-CSRFToken`?
- [ ] Нет `|safe` в шаблоне?
- [ ] Пользовательский ввод не попадает в `|safe` или `mark_safe()`?
