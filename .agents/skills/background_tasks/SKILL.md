---
name: background_tasks
description: Правила работы с Celery, Redis и фоновыми задачами (асинхронная генерация документов, отправка email).
---

# Фоновые задачи (Celery) в StudCareer

> **Статус:** Celery настроен в зависимостях (`requirements/base.txt`), но активно используется с **Фазы 4+**.

## 1. Зачем нужен Celery

Все долгие, блокирующие операции должны выполняться в фоне, чтобы не тормозить HTTP-ответы (особенно HTMX, которые должны быть моментальными).

**Что выносить в задачи:**
- ✅ Отправка Email-уведомлений (регистрация, изменение статуса отклика)
- ✅ Генерация PDF/DOCX (если станет узким местом — сейчас синхронно)
- ✅ Рассылки в Telegram (в будущем)
- ✅ Массовые операции (импорт/экспорт данных)

**Что НЕ выносить:**
- ❌ Простые CRUD-операции
- ❌ Создание `InternshipExperience` при completion (должно быть синхронным — через сигнал)
- ❌ Рендер шаблонов (всегда синхронно)

---

## 2. Инфраструктура

| Компонент | Назначение | URL |
|---|---|---|
| **Redis** (broker) | Очередь задач | `redis://localhost:6379/1` |
| **Redis** (backend) | Хранение результатов | `redis://localhost:6379/2` |

> ⚠️ Без запущенного Redis задачи Celery молча «зависнут» — ни ошибок, ни логов. Перед тестированием: `redis-cli ping` → `PONG`.

---

## 3. Конфигурация Celery

### Файл `config/celery.py` (создать при старте Фазы 4)
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('studcareer')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # Автоматически найдёт tasks.py во всех apps
```

### Файл `config/__init__.py` (добавить)
```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### Настройки в `config/settings/base.py` (добавить)
```python
# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300  # 5 минут макс на задачу
```

---

## 4. Правила написания задач

### Где хранить
Задачи определяются в `tasks.py` внутри каждого приложения:
```
apps/
├── notifications/
│   └── tasks.py     ← email-уведомления
├── profiles/
│   └── tasks.py     ← генерация PDF/DOCX (если будет async)
```

### Декоратор
Используйте **`@shared_task`** (не `@app.task`!) — это позволяет задаче работать независимо от конкретного Celery app:

```python
from celery import shared_task

@shared_task
def send_notification_task(user_id, message):
    """Отправить email пользователю."""
    from apps.accounts.models import User
    user = User.objects.get(id=user_id)
    # ... отправка email ...
```

### ⚠️ Золотое правило: передавай только ID, не объекты!
```python
# ❌ НЕПРАВИЛЬНО — ORM-объект нельзя сериализовать в JSON
send_notification_task.delay(user)

# ✅ ПРАВИЛЬНО — передай только primary key
send_notification_task.delay(user.id)
```

**Почему:** Celery сериализует аргументы задачи в JSON для отправки через Redis. ORM-объекты содержат несериализуемые связи и кэши. Внутри задачи объект получается заново из БД.

---

## 5. Пример полной задачи (с retry)

```python
# apps/notifications/tasks.py

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # секунд между попытками
    autoretry_for=(ConnectionError, TimeoutError),
)
def send_status_change_email(self, participant_id, new_status):
    """
    Уведомить студента об изменении статуса отклика.
    Вызывается: при смене InternshipParticipant.status.
    """
    from apps.internships.models import InternshipParticipant
    from django.core.mail import send_mail

    try:
        participant = InternshipParticipant.objects.select_related(
            'student', 'internship__company'
        ).get(id=participant_id)
    except InternshipParticipant.DoesNotExist:
        logger.warning(f"Participant {participant_id} not found, skipping email")
        return

    send_mail(
        subject=f'Статус вашего отклика изменён: {new_status}',
        message=f'Ваш отклик на "{participant.internship.title}" теперь имеет статус: {new_status}.',
        from_email='noreply@studcareer.uz',
        recipient_list=[participant.student.email],
    )
    logger.info(f"Email sent to {participant.student.email} for status={new_status}")
```

### Вызов из view/signal:
```python
from apps.notifications.tasks import send_status_change_email

# Не блокирует HTTP-ответ — задача уходит в Redis
send_status_change_email.delay(participant.id, 'active')
```

---

## 6. Запуск и мониторинг

### Локальная разработка
```powershell
# Терминал 1: Redis
redis-server

# Терминал 2: Celery worker
venv\Scripts\celery -A config worker -l info

# Терминал 3: Django
venv\Scripts\python manage.py runserver
```

### Проверка что Redis работает
```powershell
redis-cli ping
# → PONG
```

### Мониторинг очереди (опционально, Фаза 5)
```powershell
# Flower — веб-UI для Celery
pip install flower
venv\Scripts\celery -A config flower
# → http://localhost:5555/
```
