---
name: deployment_checklist
description: Чеклист перед деплоем на продакшен — переменные окружения, collectstatic, Nginx, Gunicorn.
---

# Чеклист деплоя на Продакшен

> Обновлено 2026-08-23: добавлен Docker-бандл — самый быстрый путь на VPS.

## 0. Docker (РЕКОМЕНДУЕМЫЙ путь)

В проекте есть `Dockerfile`, `docker-compose.yml` (web + PostgreSQL 16 + Redis 7 + celery worker), `.dockerignore`, `requirements/production.txt` (gunicorn). Статика отдаётся через WhiteNoise — Nginx не обязателен на старте.

```bash
git clone <repo> && cd studcareer
cp .env.example .env
nano .env   # SECRET_KEY, ALLOWED_HOSTS=ваш-домен, DB_PASSWORD, SECURE_SSL_REDIRECT
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

Порт 8000 наружу; далее Nginx/Caddy как reverse-proxy + HTTPS (Certbot).
Медиа в volume `media_files`, БД в `pgdata`.

⚠️ `SECURE_SSL_REDIRECT=True` включать только после настройки HTTPS (иначе цикл
редиректов). За прокси нужен X-Forwarded-Proto — SECURE_PROXY_SSL_HEADER уже настроен.

---

## 1. Переменные окружения (`.env`)
Никогда не храни секреты в коде. На продакшене все чувствительные данные — в `.env`:

```env
SECRET_KEY=super-secret-random-string-here
DEBUG=False
ALLOWED_HOSTS=studcareer.uz,www.studcareer.uz

DATABASE_URL=postgresql://user:pass@localhost:5432/studcareer_db

CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@studcareer.uz
EMAIL_HOST_PASSWORD=smtp-password
```

---

## 2. Pre-deploy чеклист

```powershell
# 1. Применить все миграции
venv\Scripts\python manage.py migrate --settings=config.settings.production

# 2. Собрать статику
venv\Scripts\python manage.py collectstatic --noinput --settings=config.settings.production

# 3. Проверка системы
venv\Scripts\python manage.py check --deploy --settings=config.settings.production
```

---

## 3. Gunicorn (WSGI-сервер)
```bash
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120 \
  --access-logfile /var/log/gunicorn/access.log
```

---

## 4. Nginx (конфиг)
```nginx
server {
    listen 80;
    server_name studcareer.uz;

    location /static/ {
        root /var/www/studcareer/staticfiles;
    }

    location /media/ {
        root /var/www/studcareer/media;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 5. Celery Worker (systemd)
```ini
[Unit]
Description=StudCareer Celery Worker

[Service]
WorkingDirectory=/var/www/studcareer
ExecStart=/var/www/studcareer/venv/bin/celery -A config worker -l info
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 6. Финальные проверки
- `[ ]` `DEBUG = False`
- `[ ]` `ALLOWED_HOSTS` заполнен
- `[ ]` HTTPS включен (Let's Encrypt / Certbot)
- `[ ]` Медиафайлы раздает Nginx, не Django
- `[ ]` Redis и Celery запущены как сервисы
- `[ ]` Логи настроены и ротируются
