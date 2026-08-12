---
name: media_and_static
description: Как работают медиафайлы (MEDIA_ROOT, MEDIA_URL, Pillow) и статика (collectstatic) в проекте.
---

# Медиафайлы и Статика (Media & Static Files)

## 1. Медиафайлы (загружаемые пользователями)
Пользователи загружают: аватарки, фото профиля, логотипы компаний.

### Настройки (`config/settings/base.py` — добавить если нет)
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Раздача в режиме разработки (`config/urls.py`)
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... все маршруты
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
> ⚠️ `static()` работает только при `DEBUG=True`. На продакшене медиафайлы должен раздавать Nginx.

### Доступ в шаблонах
```html
{% if profile.photo %}
  <img src="{{ profile.photo.url }}" alt="Фото">
{% endif %}
```

---

## 2. Pillow
Обязателен для всех `ImageField`. Уже включён в `requirements/base.txt`.  
Если забыл установить → `pip install Pillow` или переустановить зависимости.

---

## 3. Статика (`static/`)
- Кастомные CSS/JS/картинки проекта лежат в `static/`.
- Tailwind CDN используется для разработки — отдельная сборка пока не нужна.

### Для продакшена
```powershell
venv\Scripts\python manage.py collectstatic
```
Собирает всю статику в папку `staticfiles/`. Nginx раздаёт оттуда.

```python
# config/settings/production.py
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
```

---

## 4. Хранилище для продакшена (django-storages)
На продакшене медиафайлы лучше хранить в S3-совместимом хранилище (например, AWS S3 или Cloudflare R2). Для этого используется `django-storages`. Это относится к Фазе 5.
