---
name: development_workflow
description: Памятка по запуску проекта, тестированию, работе с миграциями и экспортом (WeasyPrint, python-docx).
---

# Воркфлоу разработки StudCareer

## 1. Первый запуск с нуля (Fresh Setup)

```powershell
# 1. Создать и активировать виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 2. Установить зависимости
pip install -r requirements/base.txt
pip install -r requirements/development.txt

# 3. Применить миграции
venv\Scripts\python manage.py migrate

# 4. Создать суперпользователя (для админки)
venv\Scripts\python manage.py createsuperuser
# Email: admin@studcareer.uz
# Role: admin (ввести вручную)

# 5. Запустить сервер
venv\Scripts\python manage.py runserver
# → http://127.0.0.1:8000/
# → http://127.0.0.1:8000/admin/ (админка)
```

---

## 2. Повседневный запуск (если venv уже есть)

```powershell
# Активировать venv и запустить сервер
venv\Scripts\activate
venv\Scripts\python manage.py runserver
```

> ⚠️ Если модели изменились с прошлого раза — сначала `makemigrations` + `migrate`.

---

## 3. Миграции

```powershell
# После ЛЮБОГО изменения моделей:
venv\Scripts\python manage.py makemigrations
venv\Scripts\python manage.py migrate

# Если нужно для конкретного приложения:
venv\Scripts\python manage.py makemigrations accounts
venv\Scripts\python manage.py migrate accounts

# Посмотреть статус миграций:
venv\Scripts\python manage.py showmigrations
```

### ⚠️ Ловушки миграций:
- **Не меняй AUTH_USER_MODEL** после первой миграции!
- При переименовании полей — Django спросит "rename X to Y?" → ответь `yes`, иначе данные потеряются.
- При удалении поля с данными — добавь `default=` или `null=True` в промежуточной миграции.

---

## 4. Тестирование

```powershell
# Запуск всех тестов
venv\Scripts\pytest

# Запуск тестов конкретного приложения
venv\Scripts\pytest apps/accounts/

# Запуск конкретного теста
venv\Scripts\pytest apps/accounts/tests.py::TestUserModel -v

# С покрытием (coverage)
venv\Scripts\pytest --cov=apps/
```

Конфигурация pytest — в `pyproject.toml`.

---

## 5. Линтинг и форматирование

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

## 6. Экспорт документов (Резюме)

### PDF (WeasyPrint)
- Сервис: `apps/profiles/services/pdf_exporter.py`
- Рендерит HTML-шаблон (например, `profiles/themes/classic.html`) и конвертирует в PDF.
- **Требует GTK на Windows!** См. `gotchas_and_known_issues`.

### DOCX (python-docx)
- Сервис: `apps/profiles/services/docx_exporter.py`
- Программная сборка документа через API python-docx.

---

## 7. i18n (интернационализация)

```powershell
# Собрать строки для перевода
venv\Scripts\python manage.py makemessages -l ru -l uz -l en

# Скомпилировать переводы
venv\Scripts\python manage.py compilemessages
```

Файлы переводов в `locale/<lang>/LC_MESSAGES/django.po`.

---

## 8. Создание нового Django-приложения

```powershell
# 1. Создать
mkdir apps\my_new_app
venv\Scripts\python manage.py startapp my_new_app apps/my_new_app

# 2. Исправить apps.py:
#    name = 'apps.my_new_app'  (НЕ просто 'my_new_app'!)

# 3. Добавить в INSTALLED_APPS (config/settings/base.py)
# 4. Создать urls.py с app_name
# 5. Подключить в config/urls.py
# 6. Обновить скиллы: api_and_urls, data_models_reference
```

---

## 9. Django Shell (для отладки)

```powershell
venv\Scripts\python manage.py shell

# Примеры:
>>> from apps.accounts.models import User
>>> User.objects.count()
>>> User.objects.create_superuser(email='test@test.com', username='test', role='admin', password='pass')
```

---

## 10. Celery (Фаза 4+)

```powershell
# Запустить Redis (в отдельном терминале)
redis-server

# Запустить Celery worker
venv\Scripts\celery -A config worker -l info

# Проверить что Redis работает
redis-cli ping
# → PONG
```

> ⚠️ Без Redis задачи Celery молча зависнут. Подробнее → `background_tasks` skill.

---

## Переменные окружения (production)

В продакшене чувствительные данные читаются из `.env`:

| Переменная | Описание | Пример |
|---|---|---|
| `DJANGO_SECRET_KEY` | Секретный ключ Django | `your-production-secret-key` |
| `DJANGO_DEBUG` | Debug mode | `False` |
| `DATABASE_URL` | PostgreSQL URL | `postgres://user:pass@host:5432/studcareer` |
| `REDIS_URL` | Redis для Celery | `redis://localhost:6379/0` |
| `ALLOWED_HOSTS` | Разрешённые хосты | `studcareer.uz,www.studcareer.uz` |
