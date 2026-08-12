---
name: coding_conventions
description: Стандарты именования файлов, переменных, URL-паттернов и структуры кода в проекте StudCareer.
---

# Соглашения по коду (Coding Conventions)

## 1. Именование

| Что | Стандарт | Пример |
|---|---|---|
| Python-классы | `PascalCase` | `StudentProfile`, `InternshipParticipant` |
| Python-функции/методы | `snake_case` | `get_or_create_profile()` |
| Django views (function) | `snake_case` с контекстом | `catalog`, `apply`, `profile_edit` |
| URL-имена | `snake_case`, через `:` | `profiles:builder`, `internships:apply` |
| Шаблоны (полные) | `snake_case.html` | `builder.html`, `catalog.html` |
| Шаблоны (partial/HTMX) | `_snake_case.html` (с `_` префиксом!) | `_internship_card.html`, `_list.html` |
| CSS-классы | Tailwind утилиты (не кастомные) | `bg-indigo-600 text-white rounded-lg` |
| Constants / choices | `UPPER_SNAKE_CASE` | `PENDING`, `VERIFIED` |
| Файлы сервисов | `snake_case` с суффиксом | `pdf_exporter.py`, `docx_exporter.py` |

---

## 2. Порядок импортов (PEP 8 + Ruff)

```python
# 1. Стандартная библиотека
import json
from functools import wraps

# 2. Django
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

# 3. Сторонние пакеты
from celery import shared_task

# 4. Локальные приложения
from apps.accounts.decorators import employer_required, student_required
from apps.internships.models import Internship
```

> Ruff автоматически сортирует импорты (`isort` встроен). Запускай `venv\Scripts\ruff check . --fix`.

---

## 3. Структура view-функции (канонический паттерн)

```python
@employer_required  # 0. Декоратор роли (вместо @login_required если нужна роль)
def my_view(request, slug):
    # 1. Получение объектов из БД
    obj = get_object_or_404(Internship, slug=slug)

    # 2. Проверка прав доступа (object-level)
    if obj.company.user != request.user:
        raise Http404  # 404, не 403 — чтобы не раскрывать существование

    # 3. Обработка POST
    if request.method == 'POST':
        form = MyForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # HTMX: вернуть partial + toast
            if request.headers.get('HX-Request'):
                response = render(request, 'app/_partial.html', {'obj': obj})
                response['HX-Trigger'] = json.dumps({
                    'show-toast': {'message': 'Сохранено!', 'type': 'success'}
                })
                return response
            return redirect('app:detail', slug=obj.slug)
    else:
        form = MyForm(instance=obj)

    # 4. GET — рендер шаблона (HTMX или полная страница)
    template = 'app/_partial.html' if request.headers.get('HX-Request') else 'app/full_page.html'
    return render(request, template, {'obj': obj, 'form': form})
```

---

## 4. Сервисный слой (services/)

Бизнес-логика (экспорт, обработка данных, внешние API) **НЕ должна** быть в views. Выносить в `services/`:

```
apps/profiles/
├── views.py          ← только HTTP-логика (request → response)
└── services/
    ├── __init__.py
    ├── pdf_exporter.py   ← бизнес-логика генерации PDF
    └── docx_exporter.py  ← бизнес-логика генерации DOCX
```

### Правила:
- View вызывает сервис, сервис возвращает результат.
- Сервисы **не знают** про `request` (не принимают его как аргумент).
- Сервисы **не рендерят** шаблоны.
- Сервисы можно вызывать из тестов, management-команд, Celery-задач.

```python
# views.py (коротко и чисто)
from apps.profiles.services.pdf_exporter import generate_resume_pdf

def export_pdf(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    pdf_bytes = generate_resume_pdf(profile)  # Сервис делает всю работу
    return HttpResponse(pdf_bytes, content_type='application/pdf')
```

---

## 5. HTMX-ответы (паттерны)

### Toast-уведомление после POST
```python
import json
from django.http import HttpResponse

response = HttpResponse(status=204)  # No Content — не нужен HTML
response['HX-Trigger'] = json.dumps({
    'show-toast': {'message': 'Отклик отправлен!', 'type': 'success'}
})
return response
```

### Partial vs Full page
```python
if request.headers.get('HX-Request'):
    return render(request, 'app/_partial.html', context)
return render(request, 'app/full_page.html', context)
```

> ⚠️ **Не используй** `request.htmx` — это атрибут `django-htmx` пакета, который мы не используем. Проверяй заголовок напрямую.

---

## 6. Создание нового приложения (чеклист)

При добавлении нового Django-приложения в `apps/`:

```markdown
1. [ ] `mkdir apps\new_app && venv\Scripts\python manage.py startapp new_app apps/new_app`
2. [ ] Исправить `apps/new_app/apps.py` — `name = 'apps.new_app'` (с prefix!)
3. [ ] Добавить `'apps.new_app'` в `INSTALLED_APPS` (`config/settings/base.py`)
4. [ ] Создать `apps/new_app/urls.py` с `app_name = 'new_app'`
5. [ ] Подключить в `config/urls.py`: `path('new_app/', include('apps.new_app.urls'))`
6. [ ] Обновить skill `api_and_urls/SKILL.md` с новыми маршрутами
7. [ ] Обновить skill `data_models_reference/SKILL.md` с новыми моделями
8. [ ] Обновить дерево файлов в `project_architecture/SKILL.md`
```

---

## 7. Линтинг и форматирование

```powershell
# Проверка
venv\Scripts\ruff check .

# Авто-исправление
venv\Scripts\ruff check . --fix

# Форматирование
venv\Scripts\ruff format .
```

Правила Ruff описаны в `pyproject.toml`. Длина строки — `100` символов.

---

## 8. Комментарии и docstrings

- **Views** — docstring обязателен (1 строка: что делает).
- **Models** — docstring на классе.
- **Сервисы** — docstring + описание аргументов если неочевидно.
- **Inline-комментарии** — только для неочевидной логики. НЕ комментируй очевидное.

```python
# ✅ Хорошо — объясняет ПОЧЕМУ
# Http404 вместо 403, чтобы не раскрывать существование эндпоинта
raise Http404

# ❌ Плохо — объясняет ЧТО (и так видно)
# Поднимаем ошибку 404
raise Http404
```
