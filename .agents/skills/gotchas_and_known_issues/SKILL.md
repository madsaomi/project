---
name: gotchas_and_known_issues
description: Список известных ловушек, частых ошибок и важных предупреждений по проекту. Читай перед тем как менять модели или настройки.
---

# Ловушки и Известные Проблемы (Gotchas)

> ⚠️ **Читай ПЕРЕД началом работы!** Каждая ловушка здесь стоила кому-то потерянного времени.
> Источники: аудит кода, WORKLOG `⚠️`-ошибки, ручная проверка.
> Последнее обновление: 2026-08-22

---

## 🔴 Критические (могут сломать проект)

### 1. `AUTH_USER_MODEL` нельзя менять после миграций
Кастомная модель `accounts.User` задана через `AUTH_USER_MODEL = 'accounts.User'` в `base.py`. **После первой миграции это поле изменить нельзя** без полного сброса БД. Не трогай это без крайней необходимости.

### 2. Все приложения в `apps/` — не в корне!
Django-приложения находятся в `apps/имя_приложения/`. Значит `AppConfig.name` должен быть `apps.accounts`, а НЕ просто `accounts`. Это уже настроено в каждом `apps.py`, но если создаешь новое приложение — обязательно исправь!

```python
# apps/my_new_app/apps.py — ПРАВИЛЬНО:
class MyNewAppConfig(AppConfig):
    name = 'apps.my_new_app'  # ← с префиксом apps.
```

### 3. WeasyPrint на Windows требует GTK
Если `generate_resume_pdf()` падает с ошибкой о GTK или Cairo — нужно установить [GTK for Windows](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer). На Linux/Mac работает из коробки.

### 4. `InternshipExperience` создается ТОЛЬКО автоматически
Не создавай `InternshipExperience` вручную напрямую. Этот объект должен создаваться только через сигнал или сервис при изменении `InternshipParticipant.status = 'completed'`. Нарушение этого правила приведет к дублям в резюме.

### 5. CSRF для HTMX POST
**РЕШЕНО (2026-08-22):** в `base.html` есть `<meta name="csrf-token">` + обработчик `htmx:configRequest`, который добавляет заголовок `X-CSRFToken` ко всем HTMX-запросам. Если пишешь сырой `fetch`/`XHR` — токен бери из этой meta. Не удаляй этот скрипт, иначе все `hx-post` начнут возвращать 403.
> ⚠️ Django test client по умолчанию НЕ проверяет CSRF — тесты не поймают такую поломку. Проверяй руками в браузере.

---

## 🟡 Важные нюансы

### 6. `ruff check --fix` ломает side-effect импорты Django
Ruff считает `import apps.internships.signals` внутри `AppConfig.ready()` «неиспользуемым» и удаляет его — сигналы перестают регистрироваться, а тесты падают неочевидным образом. Если гоняешь `--fix`, всегда проверяй `apps/*/apps.py` на месте ли импорт сигналов (должен быть с `# noqa: F401`).

### 6.1. У django.test.Client нет атрибута `.user`
После `force_login` обращайся к пользователю через фикстуру (`employer_user`), а не `auth_employer_client.user` — будет `AttributeError`.

### 6.2. LogoutView в Django 5 принимает только POST
Ссылка `<a href="{% url 'accounts:logout' %}">` даст 405. В navbar logout сделан inline-формой с `{% csrf_token %}`. Не возвращай `<a>`-ссылку.

### 6.3. Фикстуры auth_*_client создают СВОИ Client()
`auth_student_client` и `auth_employer_client` НЕ используют общий fixture `client` — раньше оба логинили один и тот же объект, и последний force_login «перелогинивал» первого: запросы студента уходили под работодателем → загадочные 404 от @student_required. Если нужна роль — бери соответствующий auth_*_client; если нужен сырой клиент — запрашивай `client`.

### 6. Pillow обязателен для ImageField
Модели `User.avatar`, `StudentProfile.photo`, `Company.logo` используют `ImageField`. Без установленного `Pillow` Django упадет с ошибкой при попытке загрузить файл. Он уже есть в `requirements/base.txt`.

### 7. MEDIA_URL и MEDIA_ROOT
**РЕШЕНО (2026-08-22):** `MEDIA_URL`/`MEDIA_ROOT` добавлены в `base.py`, раздача в DEBUG — в `config/urls.py`. На проде медиа раздаёт Nginx (см. deployment_checklist). `STATIC_ROOT = staticfiles/` для collectstatic тоже настроен.

### 8. SQLite не подходит для продакшена
Локально используем `SQLite` (для скорости разработки). На продакшене обязательно PostgreSQL — он описан в `config/settings/production.py`.

### 9. Celery не работает без Redis
Если Redis не запущен, задачи Celery молча «зависнут». Перед тестированием фоновых задач убедись что Redis запущен: `redis-cli ping` → должен ответить `PONG`.

### 10. Не используй `request.htmx` — пакет `django-htmx` не установлен
Некоторые примеры в интернете используют `request.htmx` для проверки HTMX-запроса. В проекте **нет** пакета `django-htmx`. Проверяй заголовок напрямую:
```python
# ✅ ПРАВИЛЬНО
if request.headers.get('HX-Request'):
    ...

# ❌ НЕПРАВИЛЬНО (AttributeError)
if request.htmx:
    ...
```

### 11. Декораторы ролей — готовы, не пиши свои!
`@student_required`, `@employer_required` **уже реализованы** в `apps/accounts/decorators.py`. Миксины для CBV — в `apps/accounts/mixins.py`. Не создавай дублирующий код, импортируй:
```python
from apps.accounts.decorators import student_required, employer_required
from apps.accounts.mixins import StudentRequiredMixin, EmployerRequiredMixin
```

---

## 🟢 Стилистические требования

### 12. Не используй `|safe` фильтр в шаблонах
Django экранирует HTML по умолчанию. Использование `{{ value|safe }}` открывает XSS-уязвимость. Единственное исключение — данные, сгенерированные самим Django (например, форматированный Markdown, обработанный на сервере).

### 13. Partial-шаблоны именуй с `_` префикса
Шаблоны, возвращаемые только для HTMX (фрагменты HTML), должны начинаться с подчеркивания: `_internship_card.html`, `_application_row.html`. Это мгновенно говорит следующему разработчику, что шаблон — частичный.

### 14. LOGIN_REDIRECT_URL
**РЕШЕНО (2026-08-22):** в `base.py` заданы `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`. Кастомные login/register дополнительно редиректят по роли (студент → мои стажировки, работодатель → Kanban).

### 15. StudentProfile обязан существовать у каждого студента
**ВАЖНО:** сигнал `apps/accounts/signals.py` автоматически создаёт `StudentProfile` для всех новых пользователей с ролью student. Без него завершение стажировки падает с 500 (сигнал опыта ссылается на `student.student_profile`). Не удаляйте этот сигнал. Если создаёте студента в обход ORM — создайте профиль вручную.

---

## 📋 Процесс обновления этого файла

При завершении задачи агент **обязан** перенести нерешённые ошибки (`⚠️`) из WORKLOG в этот файл:
1. Найди `⚠️` в секции `**Ошибки:**` своей записи.
2. Добавь в соответствующую секцию здесь (🔴/🟡/🟢).
3. Укажи номер (инкрементальный).
4. Опиши проблему, причину и (если есть) обходное решение.
