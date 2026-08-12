---
name: api_and_urls
description: Полная карта всех URL-маршрутов проекта StudCareer на текущий момент.
---

# Карта URL-маршрутов (API & URLs)

> **Статус:** ✅ Верифицировано с реальным кодом. Актуально на конец Фазы 2.
> Последняя проверка: 2026-08-12

## Корневой роутер (`config/urls.py`)

```python
urlpatterns = [
    path('admin/',      admin.site.urls),
    path('accounts/',   include('apps.accounts.urls')),   # app_name='accounts'
    path('profiles/',   include('apps.profiles.urls')),    # app_name='profiles'
    path('companies/',  include('apps.companies.urls')),   # app_name='companies'
    path('',            include('apps.core.urls')),        # app_name='core'
]
```

> ⚠️ При Фазе 3 нужно добавить: `path('internships/', include('apps.internships.urls'))`

---

## `accounts` — Аутентификация

| URL | `name` (reverse) | View | Метод | Доступ |
|---|---|---|---|---|
| `/accounts/login/` | `accounts:login` | `login_view` | GET, POST | Все |
| `/accounts/register/` | `accounts:register` | `register_view` | GET, POST | Все |

> 🔜 Планируется: `/accounts/logout/`, `/accounts/password-reset/`

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

## `internships` — Стажировки (⏳ Фаза 3 — ещё не реализовано)

> Модели мигрированы, views пустые. Ниже — **планируемые** маршруты из `phase3_detailed_plan`.

| URL | `name` (reverse) | View | Метод | Доступ |
|---|---|---|---|---|
| `/internships/` | `internships:catalog` | `catalog` | GET | Все |
| `/internships/create/` | `internships:create` | `create` | GET, POST | `@employer_required` |
| `/internships/<slug>/` | `internships:detail` | `detail` | GET | Все |
| `/internships/<slug>/edit/` | `internships:edit` | `edit` | GET, POST | `@employer_required` + owner |
| `/internships/<slug>/apply/` | `internships:apply` | `apply` | POST | `@student_required` |
| `/dashboard/` | `internships:dashboard` | `dashboard` | GET | `@employer_required` |

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
