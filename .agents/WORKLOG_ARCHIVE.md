# 📦 Архив Журнала Работы

> Сюда переносятся **завершённые** (`✅ DONE`) записи из `WORKLOG.md`.
> Актуальные задачи → [WORKLOG.md](file:///.agents/WORKLOG.md)

---

## 📜 АРХИВНЫЕ ЗАПИСИ

---

### [2026-08-12 06:00] Задача: Фаза 1 — Базовый каркас проекта
**Статус:** ✅ DONE
**Агент:** Antigravity (Gemini)
**Что делал:**
- Создал venv, `requirements/base.txt`, `requirements/development.txt`.
- Инициализировал Django проект `config/`.
- Разделил настройки на `base.py`, `development.py`, `production.py`.
- Исправил `BASE_DIR` (3 уровня вверх от `config/settings/base.py`).
- Создал приложение `apps/accounts` с кастомной моделью `User` (роли: student, employer, admin).
- Применил миграции (`accounts.0001_initial` + все встроенные).
- Создал шаблоны: `base.html`, `navbar.html`, `footer.html`, `toast.html`.
- Создал приложение `apps/core` с главной страницей и роутером.
- Настроил `pyproject.toml` (Ruff, pytest), `.pre-commit-config.yaml`.
- Настроил i18n (ru, uz, en), `LOCALE_PATHS`.

**Результат:** ✅ Сервер поднимается, главная страница работает, `/accounts/login/` и `/accounts/register/` доступны.

---

### [2026-08-12 06:18] Задача: Фаза 2 — Профили, Компании, Стажировки (модели)
**Статус:** ✅ DONE
**Агент:** Antigravity (Gemini)
**Что делал:**
- Создал `apps/profiles` с моделями: `StudentProfile`, `Skill`, `LanguageSkill`, `InternshipExperience`.
- Создал `apps/companies` с моделью `Company` (verification_status: pending/verified/rejected).
- Создал `apps/internships` с моделями: `Category`, `Internship`, `InternshipSkill`, `InternshipParticipant`.
- Зарегистрировал все модели в `admin.py`.
- Применил миграции для всех трёх приложений.
- Реализовал views и шаблоны для профиля студента (builder/viewer).
- Реализовал сервисы экспорта в PDF (WeasyPrint) и DOCX (python-docx).
- Реализовал views и шаблоны для профиля компании (edit/view).
- Подключил `/profiles/` и `/companies/` в `config/urls.py`.

**Результат:** ✅ Все модели мигрированы. Конструктор резюме и страница компании работают.

---

### [2026-08-12 06:28] Задача: Создание базы знаний агентов (.agents/)
**Статус:** ✅ DONE
**Агент:** Antigravity (Gemini → Claude Sonnet)
**Что делал:**
- Создал `.agents/AGENTS.md` с кратким обзором проекта и Roadmap.
- Создал 13 специализированных skills в `.agents/skills/`:
  `project_architecture`, `ui_ux_guidelines`, `development_workflow`,
  `business_logic`, `background_tasks`, `security_and_auth`,
  `data_models_reference`, `templates_structure`, `api_and_urls`,
  `gotchas_and_known_issues`, `testing_guide`, `phase3_detailed_plan`,
  `media_and_static`, `i18n_guide`, `coding_conventions`, `deployment_checklist`.
- Создал `WORKLOG.md` (этот файл) — протокол непрерывной работы агентов.

**Результат:** ✅ База знаний создана. Любой новый агент может быстро войти в контекст.

---

### [2026-08-12 07:28] Задача: Реализация декораторов ролей и миксинов (security_and_auth)
**Статус:** ✅ DONE
**Агент:** Antigravity (Gemini 3.6 Flash)
**Контекст:** Реализация декораторов ролей и mixins в `apps/accounts/` согласно рекомендациям из аудита.
**Что делал:**
- [x] Создал `apps/accounts/decorators.py` (@role_required, @student_required, @employer_required)
- [x] Создал `apps/accounts/mixins.py` (RoleRequiredMixin, StudentRequiredMixin, EmployerRequiredMixin)
- [x] Написал unit-тесты в `apps/accounts/tests.py`

**Прогресс:**
- ✅ [07:28] Создал `apps/accounts/decorators.py`
- ✅ [07:28] Создал `apps/accounts/mixins.py`
- ✅ [07:28] Написал комплексные тесты безопасности в `apps/accounts/tests.py`

**Результат:** ✅ Все декораторы и миксины разграничения прав доступа реализованы и протестированы.

---

### [2026-08-12 07:48] Задача: Глубокое улучшение базы знаний .agents/
**Статус:** ✅ DONE
**Агент:** Antigravity (Gemini 3.1 Pro)
**Контекст:** Аудит показал тонкие скиллы и рассинхронизацию с кодом. Улучшаю все 17 скиллов.
**Что сделал:**
- [x] Обогатить `ui_ux_guidelines` — добавить CDN-версии, tailwind.config, цветовую палитру, примеры компонентов, адаптивность
- [x] Обогатить `business_logic` — добавить матрицу прав, жизненный цикл InternshipParticipant (диаграмма), правила для каждой роли
- [x] Обогатить `background_tasks` — добавить структуру Celery-конфига, пример полной задачи, retry-стратегию, мониторинг
- [x] Обогатить `testing_guide` — добавить паттерн тестирования HTMX, тесты ролей, conftest.py
- [x] Обогатить `api_and_urls` — верифицировать с реальным кодом, добавить колонку "Декоратор"
- [x] Обогатить `coding_conventions` — добавить структуру сервисного слоя, паттерн HTMX-ответа, импорты
- [x] Синхронизировать `security_and_auth` — убрать пометку "нужно создать", декораторы уже реализованы
- [x] Обогатить `templates_structure` — добавить Tailwind config из base.html, CSRF-настройку HTMX
- [x] Обогатить `gotchas_and_known_issues` — добавить ловушки из WORKLOG, пометку о реализованных декораторах

**Прогресс:**
- ✅ [07:54] Улучшены все 9 целевых навыков, база знаний полностью актуализирована.

**Ошибки:**
_(не было)_

**Решения:**
- Все `SKILL.md` файлы перезаписаны с гораздо более подробным содержанием.

---

### [2026-08-12 01:00] Задача: Фаза 3 — Каталог стажировок и отклики (из очереди)
**Статус:** ✅ DONE
**Агент:** Antigravity (Gemini 3.1 Pro)
**Результат:**
- Созданы `apps/internships/urls.py` и `views.py`.
- Реализованы шаблоны: `catalog.html`, `detail.html`, `create.html`, `dashboard.html` и partials для HTMX.
- Добавлены сигналы `apps/internships/signals.py` для создания `InternshipExperience` при завершении стажировки.
- Обновлен `navbar.html` и `config/urls.py`.
- Написаны базовые тесты в `apps/internships/tests.py`.

---

### [2026-08-12 01:10] Задача: Фаза 4 — Уведомления и Сообщения (из очереди)
**Статус:** ✅ DONE
**Агент:** Antigravity (Gemini 3.1 Pro)
**Контекст:** Настройка Celery для фоновых задач (уведомления) и разработка системы чатов (messaging) между студентом и работодателем.
**Результат:**
- Настроен Celery с использованием Redis.
- Создано приложение `notifications` с задачей `send_status_change_email` (вызывается из сигналов `internships`).
- Создано приложение `messaging` (модели `Conversation` и `Message`).
- Реализованы views и шаблоны для чатов (HTMX-поллинг).
- Ссылка "Сообщения" добавлена в navbar.
- Найден баг с импортом WeasyPrint при локальной разработке на Windows (блокировал manage.py команды). Исправлен локальным импортом внутри функции.

**Ошибки:**
- WeasyPrint падал при импорте из-за отсутствия GTK в Windows, что ломало все команды Django. 
- *Решение:* Импорт `weasyprint` перенесён внутрь функции `generate_resume_pdf`.

---

### [2026-08-22 17:07] Задача: Подъём окружения (venv) + старт Фазы 5
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Новая задача. Пользователь просил работать «по порядку»: сначала окружение (venv не найден), затем Фаза 5.
**Что сделал:**
- [x] Создал venv (`venv\`) на Python 3.14, установил requirements base + development
- [x] Миграции применены, `manage.py check` чисто, smoke runserver 200
- [x] Создал корневой `conftest.py`: фабрики User/Company/Internship (factory_boy), фикстуры student_user/employer_user/internship_factory, autouse CELERY_TASK_ALWAYS_EAGER
- [x] Починил 2 бага: navbar ссылался на несуществующий `companies:list`; signals.py использовал несуществующее поле `updated_at`
- [x] Ruff: per-file-ignores (migrations E501, settings F403/F405), чистка до нуля замечаний

**Ошибки:**
- Тесты Фазы 3/4 ссылались на несуществующие фикстуры — не было conftest.py. *Решение:* создал корневой conftest.
- `ruff --fix` удалил side-effect импорт сигналов в apps.py. *Решение:* вернул с `# noqa: F401` (см. gotchas #6).

**Решения:**
- Удалил из navbar мёртвую ссылку «Компании» (`companies:list`) — каталога компаний нет и не запланирован.
- Celery в тестах — через CELERY_TASK_ALWAYS_EAGER (без Redis).

---
