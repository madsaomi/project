---
name: gotchas_and_known_issues
description: Список известных ловушек, частых ошибок и важных предупреждений по проекту. Читай перед тем как менять модели или настройки.
---

# Ловушки и Известные Проблемы (Gotchas)

> ⚠️ **Читай ПЕРЕД началом работы!** Каждая ловушка здесь стоила кому-то потерянного времени.
> Источники: аудит кода, WORKLOG `⚠️`-ошибки, ручная проверка.
> Последнее обновление: 2026-08-12

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

### 5. CSRF для HTMX POST НЕ настроен в base.html!
В текущем `base.html` **отсутствует** глобальный перехват CSRF-токена для HTMX. Это значит что ЛЮБОЙ `hx-post` вернёт **403 Forbidden**. 

**Решение:** Добавить в `base.html` перед `{% block extra_scripts %}`:
```html
<meta name="csrf-token" content="{{ csrf_token }}">
<script>
  document.body.addEventListener('htmx:configRequest', (e) => {
    e.detail.headers['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]').content;
  });
</script>
```
> 🔧 **Статус:** Нужно исправить перед стартом Фазы 3 (первый HTMX POST будет в каталоге стажировок).

---

## 🟡 Важные нюансы

### 6. Pillow обязателен для ImageField
Модели `User.avatar`, `StudentProfile.photo`, `Company.logo` используют `ImageField`. Без установленного `Pillow` Django упадет с ошибкой при попытке загрузить файл. Он уже есть в `requirements/base.txt`.

### 7. MEDIA_URL и MEDIA_ROOT не настроены!
В `config/settings/base.py` **отсутствуют** `MEDIA_URL` и `MEDIA_ROOT`. Без этого загружаемые файлы (аватарки, логотипы) не будут сохраняться и раздаваться. 

**Решение:** Добавить в `base.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

И в `config/urls.py` (для DEBUG=True):
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

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

### 14. LOGIN_REDIRECT_URL не настроен
По умолчанию Django перенаправляет на `/accounts/profile/` после входа. Нужно настроить:
```python
# config/settings/base.py
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
```

---

## 📋 Процесс обновления этого файла

При завершении задачи агент **обязан** перенести нерешённые ошибки (`⚠️`) из WORKLOG в этот файл:
1. Найди `⚠️` в секции `**Ошибки:**` своей записи.
2. Добавь в соответствующую секцию здесь (🔴/🟡/🟢).
3. Укажи номер (инкрементальный).
4. Опиши проблему, причину и (если есть) обходное решение.
