---
name: api_and_urls
description: Полная карта всех URL-маршрутов проекта StudCareer на текущий момент.
---

# Карта URL-маршрутов (API & URLs)

> **Статус:** ✅ Верифицировано с реальным кодом. Актуально на Фазу 5.1.
> Последняя проверка: 2026-08-22

## Корневой роутер (`config/urls.py`)

```python
urlpatterns = [
    path('admin/',       admin.site.urls),
    path('accounts/',    include('apps.accounts.urls')),      # app_name='accounts'
    path('profiles/',    include('apps.profiles.urls')),      # app_name='profiles'
    path('companies/',   include('apps.companies.urls')),     # app_name='companies'
    path('internships/', include('apps.internships.urls')),   # app_name='internships'
    path('messages/',    include('apps.messaging.urls')),     # app_name='messaging'
    path('notifications/', include('apps.notifications.urls')), # app_name='notifications'
    path('',             include('apps.core.urls')),          # app_name='core'
]
```

---

## `notifications` — In-app уведомления

| URL | `name` (reverse) | View | Метод | Доступ |
|---|---|---|---|---|
| `/notifications/` | `notifications:list` | `notification_list` | GET | `@login_required` |
| `/notifications/mark-read/` | `notifications:mark_all_read` | `mark_all_read` | **POST** | `@login_required` |

> Бейдж непрочитанных в navbar через context processor `apps.notifications.context_processors.unread_notifications`.
> Уведомления создаются в сигнале `apps/internships/signals.py`: новый отклик → работодателю, смена статуса → студенту.

---

## `accounts` — Аутентификация

| URL | `name` (reverse) | View | Метод | Доступ |
|---|---|---|---|---|
| `/accounts/login/` | `accounts:login` | `login_view` | GET, POST | Все |
| `/accounts/register/` | `accounts:register` | `register_view` | GET, POST | Все |
| `/accounts/logout/` | `accounts:logout` | `LogoutView` (Django) | **POST** | Авторизованные |
| `/accounts/password-reset/` | `accounts:password_reset` | `PasswordResetView` | GET, POST | Все |
| `/accounts/password-reset/done/` | `accounts:password_reset_done` | `PasswordResetDoneView` | GET | Все |
| `/accounts/password-reset/<uidb64>/<token>/` | `accounts:password_reset_confirm` | `PasswordResetConfirmView` | GET, POST | Все |
| `/accounts/password-reset/complete/` | `accounts:password_reset_complete` | `PasswordResetCompleteView` | GET | Все |

> ⚠️ LogoutView принимает только POST — в navbar это inline-форма с `{% csrf_token %}`, НЕ `<a href>`.
> После регистрации: студент → каталог, работодатель → профиль компании.
> После входа: студент → «Мои стажировки», работодатель → Kanban.
> Password-reset: встроенные auth-views Django; в dev письмо падает в консоль сервера, на проде — SMTP. Confirm-view при валидном токене редиректит на session-based `set-password/` (норма Django 5).

---

## `core` — Общие страницы

| URL | `name` (reverse) | View | Метод | Доступ |
|---|---|---|---|---|
| `/` | `core:home` | `home` | GET | Все |

---

## `profiles` — Резюме студентов

| URL | `name` (reverse) | View | Метод | Доступ |
|---|---|---|---|---|
| `/profiles/builder/` | `profiles:builder` | `builder` | GET, POST | `@login_required` |
| `/profiles/<int:pk>/` | `profiles:viewer` | `viewer` | GET | Все |
| `/profiles/<int:pk>/pdf/` | `profiles:export_pdf` | `export_pdf` | GET | Все |
| `/profiles/<int:pk>/docx/` | `profiles:export_docx` | `export_docx` | GET | Все |

---

## `companies` — Профили компаний

| URL | `name` (reverse) | View | Метод | Доступ |
|---|---|---|---|---|
| `/companies/edit/` | `companies:profile_edit` | `profile_edit` | GET, POST | `@login_required` |
| `/companies/<int:pk>/` | `companies:profile_view` | `profile_view` | GET | Все |

---

## `internships` — Стажировки

| URL | `name` (reverse) | View | Метод | Доступ |
|---|---|---|---|---|
| `/internships/` | `internships:catalog` | `catalog` | GET | Все (HTMX → `_list.html`) |
| `/internships/create/` | `internships:create` | `create` | GET, POST | `@employer_required` (+наличие company) |
| `/internships/dashboard/` | `internships:dashboard` | `dashboard` | GET | `@employer_required` |
| `/internships/my/` | `internships:my_internships` | `my_internships` | GET | `@student_required` |
| `/internships/participants/<int:pk>/status/` | `internships:update_status` | `update_participant_status` | **POST** | `@employer_required` + owner |
| `/internships/<slug>/edit/` | `internships:edit` | `edit` | GET, POST | `@employer_required` + owner |
| `/internships/<slug>/` | `internships:detail` | `detail` | GET | Все (только is_active=True) |
| `/internships/<slug>/apply/` | `internships:apply` | `apply` | POST | `@student_required` |

> ⚠️ `update_status`: object-level проверка (`participant.internship.company.user == request.user`, иначе 404) +
> валидация переходов статусов (`ALLOWED_TRANSITIONS` во views.py). Возвращает partial карточки + toast.
> ⚠️ `create/edit` используют общий шаблон `form.html`; slug генерируется автоматически из title.
> Снятие галочки «Активна» в edit закрывает набор: вакансия исчезает из каталога и detail отдаёт 404.

---

## `messaging` — Чаты

| URL | `name` (reverse) | View | Метод | Доступ |
|---|---|---|---|---|
| `/messages/` | `messaging:list` | `chat_list` | GET | `@login_required` |
| `/messages/<int:pk>/` | `messaging:detail` | `chat_detail` | GET | `@login_required` + участник |
| `/messages/<int:pk>/send/` | `messaging:send` | `send_message` | POST | `@login_required` + участник |

---

## Быстрый поиск URL (для `reverse()`)

```python
# В views / шаблонах:
from django.urls import reverse

reverse('accounts:login')                       # → /accounts/login/
reverse('profiles:builder')                     # → /profiles/builder/
reverse('profiles:viewer', kwargs={'pk': 1})    # → /profiles/1/
reverse('profiles:export_pdf', kwargs={'pk': 1})# → /profiles/1/pdf/
reverse('companies:profile_edit')               # → /companies/edit/
reverse('companies:profile_view', kwargs={'pk': 1}) # → /companies/1/
```

```html
<!-- В шаблонах: -->
{% url 'accounts:login' %}
{% url 'profiles:viewer' pk=profile.pk %}
{% url 'companies:profile_view' pk=company.pk %}
```

---

## Обновление этого файла

При добавлении новых маршрутов:
1. Добавь строку в соответствующую таблицу.
2. Укажи декоратор/доступ.
3. Обнови секцию «Быстрый поиск URL».
