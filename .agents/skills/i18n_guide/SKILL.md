---
name: i18n_guide
description: Руководство по интернационализации — как добавлять переводы (ru/uz/en), пересобирать каталоги через polib.
---

# Интернационализация (i18n Guide)

> ⚠️ Обновлено 2026-08-22: на Windows нет GNU gettext, поэтому makemessages/compilemessages
> НЕ работают. Используется pure-python пайплайн через polib — см. раздел 4.

## 1. Текущая настройка

В `config/settings/base.py`:
```python
LANGUAGE_CODE = 'ru'   # исходные строки в коде — русские, ru.mo не нужен
LANGUAGES = [('ru', 'Русский'), ('uz', 'Узбекский'), ('en', 'English')]
LOCALE_PATHS = [BASE_DIR / 'locale']
```

Подключено:
- `LocaleMiddleware` (после SessionMiddleware) — выбор языка по cookie `django_language`
- `/i18n/setlang/` (POST `language=...`) — встроенный `set_language`, переключатель в navbar
- Context processor `django.template.context_processors.i18n` — даёт `LANGUAGES`/`LANGUAGE_CODE` в шаблоны

## 2. Добавление переводимых строк

### В шаблонах
```html
{% load i18n %}
<h1>{% translate "Каталог стажировок" %}</h1>
```

### В Python-коде
```python
from django.utils.translation import gettext_lazy as _
```

## 3. Что уже переведено

Navbar, footer, home, login/register/password-reset (все 4 страницы),
заголовки и кнопки catalog / my_internships / dashboard.
Остальные страницы при отсутствии строки в каталоге показывают русский msgid — это норма.

## 4. Сборка переводов (polib pipeline)

1. Обернули новую строку в `{% translate "..." %}`.
2. Открыли `scripts/build_translations.py`, добавили строку в оба словаря CATALOGS (`'uz'` и `'en'`).
3. Запустили:
```powershell
venv\Scripts\python.exe scripts\build_translations.py
```
Скрипт перегенерирует `locale/{uz,en}/LC_MESSAGES/django.po` + компилирует `django.mo`.

## 5. Проверка

```powershell
curl.exe -s -H "Cookie: django_language=en" http://127.0.0.1:8000/
# ждём lang="en" и переведённый navbar
```

Тесты: `apps/accounts/tests.py::I18nTestCase` — переключение en/uz через POST setlang + cookie.

## 6. Ловушки

- **PowerShell портит кириллицу** в UTF-8 файлах без BOM (`Get-Content`/`Set-Content` без `-Encoding utf8`).
  Шаблоны править только edit-инструментом или Write.
- **Invoke-WebRequest игнорирует** ручной заголовок `Cookie` — для проверки языков использовать `curl.exe`.
- `$home` — зарезервированная переменная PowerShell, не использовать как имя переменной.
- Если строка есть в шаблоне, но её нет в CATALOGS → покажется русский текст (fallback на msgid), ничего не сломается.
