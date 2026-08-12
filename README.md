# StudCareer — Платформа Стажировок для Студентов

<p align="center">
  <strong>Трекер стажировок, а не доска вакансий.</strong><br>
  Студент проходит стажировку — она автоматически добавляется в его цифровое резюме.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/django-5.2-green?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/celery-5.3-37814A?logo=celery&logoColor=white" alt="Celery">
  <img src="https://img.shields.io/badge/htmx-1.9-3366CC" alt="HTMX">
  <img src="https://img.shields.io/badge/tailwindcss-3.x-06B6D4?logo=tailwindcss&logoColor=white" alt="Tailwind">
</p>

---

## 📋 О проекте

**StudCareer** — это веб-платформа, которая связывает студентов без опыта и компании, предлагающие стажировки. Ключевое отличие от обычных job-бордов: пройдённая стажировка **автоматически** становится частью цифрового резюме студента.

### Ключевые возможности

| Для студентов | Для работодателей |
|---|---|
| 🔍 Каталог стажировок с фильтрами | 📝 Создание и управление стажировками |
| 📄 Конструктор резюме (PDF / DOCX экспорт) | 📊 Kanban-доска для управления откликами |
| 💬 Чат с работодателем | 💬 Чат со студентами |
| 🏆 Автоматическое добавление опыта в резюме | 📧 Email-уведомления о новых откликах |

---

## 🏗 Архитектура

```
studcareer/
├── apps/
│   ├── accounts/       # Кастомная User модель, авторизация, роли
│   ├── core/           # Главная страница, ToS, Privacy Policy
│   ├── profiles/       # Профиль студента, конструктор резюме, PDF/DOCX
│   ├── companies/      # Профиль компании, управление
│   ├── internships/    # Каталог, отклики, Kanban-доска, сигналы
│   ├── notifications/  # Celery-задачи для email-уведомлений
│   └── messaging/      # Чат между студентом и компанией
├── config/
│   ├── settings/       # base / development / production
│   ├── celery.py       # Конфигурация Celery
│   └── urls.py
├── templates/          # Django-шаблоны (Tailwind + HTMX + Alpine.js)
├── requirements/       # base.txt / development.txt
└── manage.py
```

### Стек технологий

- **Backend:** Django 5.2, Celery 5.3, Redis
- **Frontend:** Tailwind CSS, HTMX, Alpine.js, Lucide Icons
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Export:** WeasyPrint (PDF), python-docx (DOCX)
- **Lint / Format:** Ruff, pre-commit

---

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.12+
- Redis (для Celery)
- GTK Runtime (для WeasyPrint PDF на Windows) — [скачать](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)

### Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/<your-username>/studcareer.git
cd studcareer

# 2. Создать и активировать виртуальное окружение
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements/development.txt

# 4. Настроить переменные окружения
cp .env.example .env
# Отредактируйте .env при необходимости

# 5. Применить миграции
python manage.py migrate

# 6. Создать суперпользователя
python manage.py createsuperuser

# 7. Запустить dev-сервер
python manage.py runserver
```

### Запуск Celery (для уведомлений)

```bash
# В отдельном терминале (убедитесь что Redis запущен)
celery -A config worker -l info -P solo    # Windows
celery -A config worker -l info            # Linux/Mac
```

---

## 🧪 Тестирование

```bash
# Запуск тестов
pytest

# Запуск с покрытием
pytest --cov=apps --cov-report=html

# Линтинг
ruff check .
ruff format --check .
```

---

## 📁 Переменные окружения

Смотрите [`.env.example`](.env.example) для полного списка. Основные:

| Переменная | Описание | По умолчанию |
|---|---|---|
| `SECRET_KEY` | Django secret key | — (обязательно) |
| `DEBUG` | Режим отладки | `True` |
| `DATABASE_URL` | URL базы данных | SQLite |
| `REDIS_URL` | URL Redis-сервера | `redis://localhost:6379/1` |
| `EMAIL_BACKEND` | Email backend | `console` |

---

## 🗺 Дорожная карта

- [x] **Фаза 1:** Каркас проекта, модель User, базовые шаблоны
- [x] **Фаза 2:** Профили студентов, компании, конструктор резюме (PDF/DOCX)
- [x] **Фаза 3:** Каталог стажировок, отклики, Kanban-доска
- [x] **Фаза 4:** Система чатов, email-уведомления через Celery
- [ ] **Фаза 5:** Аналитика, дашборды, SEO, полировка UI

---

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку (`git checkout -b feature/awesome-feature`)
3. Закоммитьте изменения (`git commit -m 'feat: add awesome feature'`)
4. Запушьте (`git push origin feature/awesome-feature`)
5. Откройте Pull Request

Перед коммитом убедитесь, что `ruff` и `pytest` проходят без ошибок.

---

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности — в файле [LICENSE](LICENSE).
