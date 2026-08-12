---
name: i18n_guide
description: Руководство по интернационализации — как добавлять переводы (ru/uz/en), запускать makemessages и compilemessages.
---

# Интернационализация (i18n Guide)

## 1. Текущая настройка
В проекте настроены 3 языка в `config/settings/base.py`:
```python
LANGUAGE_CODE = 'ru'
LANGUAGES = [('ru', 'Русский'), ('uz', 'Узбекский'), ('en', 'English')]
LOCALE_PATHS = [BASE_DIR / 'locale']
```
Переводы хранятся в `locale/`.

---

## 2. Добавление переводимых строк

### В Python-коде (views, models)
```python
from django.utils.translation import gettext_lazy as _

class Company(models.Model):
    name = models.CharField(_('Название компании'), max_length=255)
```

### В шаблонах Django
```html
{% load i18n %}
<h1>{% trans "Найди свою стажировку" %}</h1>

{% blocktrans with name=user.full_name %}
  Привет, {{ name }}! Добро пожаловать на StudCareer.
{% endblocktrans %}
```

---

## 3. Генерация файлов переводов

```powershell
# Собирает все строки с переводами из кода и шаблонов
venv\Scripts\python manage.py makemessages -l ru
venv\Scripts\python manage.py makemessages -l uz
venv\Scripts\python manage.py makemessages -l en

# Компилирует .po файлы в .mo (бинарный формат для Django)
venv\Scripts\python manage.py compilemessages
```

Файлы хранятся так:
```
locale/
├── ru/LC_MESSAGES/django.po
├── uz/LC_MESSAGES/django.po
└── en/LC_MESSAGES/django.po
```

---

## 4. Переключение языка
Добавить в `config/urls.py`:
```python
from django.conf.urls.i18n import i18n_patterns

urlpatterns += i18n_patterns(
    path('', include('apps.core.urls')),
    # ...
)
```
Это добавит языковой префикс: `/ru/`, `/uz/`, `/en/`.
