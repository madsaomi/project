# 📋 Журнал Работы Агентов (WORKLOG)

> **ПРАВИЛО:** Каждый агент ОБЯЗАН читать этот файл в начале работы и записывать свои задачи.
> Записи **НИКОГДА** не удаляются — только добавляются снизу. Это **append-only** история.
> Полный протокол → `.agents/skills/worklog_protocol/SKILL.md`
> 📦 Архив завершённых задач → [WORKLOG_ARCHIVE.md](file:///.agents/WORKLOG_ARCHIVE.md)
> Последняя архивация: 2026-08-26 (перенесено 13 записей)

---

## 🟢 СТАТУСЫ
| Статус | Значение |
|---|---|
| `✅ DONE` | Задача полностью выполнена, не трогать |
| `🔄 IN_PROGRESS` | Задача выполняется (или агент оборвался). **Проверь `Прогресс:` и код** |
| `⏸️ CONTINUED_BY_NEXT` | Агент оборвался, работу продолжил другой (см. ссылку) |
| `⏳ PENDING` | Задача в очереди, ещё не начата |
| `❌ BLOCKED` | Задача заблокирована (нужна информация / ручное действие) |

---

## 🟡 КРАТКИЙ ПРОТОКОЛ

### При старте:
1. Прочитай этот файл ПОЛНОСТЬЮ.
2. Найди `🔄 IN_PROGRESS` — это неоконченная работа. Прочитай её `**Прогресс:**`, `**Ошибки:**` и `**Решения:**`.
3. Проверь код (`grep_search`/`view_file`), чтобы подтвердить, что указанное в прогрессе существует.
4. Закрой чужую запись (`⏸️ CONTINUED_BY_NEXT` или `✅ DONE`) и создай СВОЮ новую.

### При начале задачи (ПЕРЕД кодом!):
```
### [2026-08-23 16:40] Задача: Админка чатов/уведомлений/верификации + закрытие дыр покрытия
**Статус:** 🔄 IN_PROGRESS
**Агент:** ox-alpha (opencode)
**Контекст:** Coverage-отчёт: 90%. Пустые admin у messaging/notifications; нет инструментов верификации компаний; непокрытые ветки: banned-login, ?next=, HX-partial чата, missing-participant в задаче.
**Что делаю:**
- [ ] Admin: Conversation/Message/Notification + actions верификации в CompanyAdmin
- [ ] Тесты на непокрытые ветки (цель ≥95% без migrations/pdf)
- [ ] Коммит

**Прогресс:**
- ✅ [17:00] Admin: Conversation (inline сообщений) / Message / Notification (readonly, без add) зарегистрированы
- ✅ CompanyAdmin: экшены verify_companies/reject_companies с verified_at и message_user
- ✅ Тесты +9: banned-логин, ?next=, role=admin→student при регистрации, дашборд без компании, повторный отклик молча, HTMX-partial чата/отправки, GET send → redirect, задача с несуществующим participant, экшены верификации
- ✅ Coverage: 90% → 91% (1573 statements); messaging/views остаётся 76% из-за редких redirect-веток
- ✅ Коммит 7877bd5. Итог: 64 passed, 0 warnings

**Ошибки:**

**Решения:**

**Результат:** ✅ apps/{messaging/admin.py,notifications/admin.py,companies/admin.py}, apps/{accounts,internships,messaging,companies,notifications}/tests.py.

---

### [2026-08-23 18:00] Задача: GitHub Actions CI
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** 64 теста и бюджеты запросов должны гоняться на каждый пуш/PR автоматически.
**Что сделал:**
- [x] `.github/workflows/ci.yml`: ruff check + ruff format --check + manage.py check + pytest --cov на python 3.12, без внешних сервисов (SQLite + eager Celery)
- [x] Коммит + пуш: проверил локально (ruff ok, 64 passed)

**Прогресс:**
- ✅ [18:10] Создал .github/workflows/ci.yml

**Ошибки:**

**Решения:**

**Результат:** ✅ .github/workflows/ci.yml
### [2026-08-23 01:10] Задача: Docker-бандл для деплоя + WhiteNoise
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Пользователь просил продолжать. Деплой без инфраструктуры невозможен, но подготовить «одну команду до прода» — можно.
**Что сделал:**
- [x] `Dockerfile` (python:3.12-slim + системные Pango/Cairo для WeasyPrint, migrate+collectstatic+gunicorn в CMD)
- [x] `docker-compose.yml`: web + postgres:16 + redis:7 + celery worker, healthchecks, volumes pgdata/media
- [x] `.dockerignore`, `requirements/production.txt` (gunicorn)
- [x] WhiteNoise: requirements/base.txt, middleware после SecurityMiddleware, WHITENOISE_USE_FINDERS/AUTOREFRESH=DEBUG (в dev статику ищет на лету — без warning о staticfiles/)
- [x] deployment_checklist skill: раздел 0 «Docker — рекомендуемый путь»
- [x] 🎉 Git найден по полному пути `C:\Program Files\Git\cmd\git.exe` (не в PATH!) — репозиторий живой, 2 коммита, user.name/email настроены. Все изменения сессии пока НЕ закоммичены (жду команды пользователя)
- [x] docker недоступен локально → compose проверен визуально; тесты 47 passed, ruff clean

**Ошибки:**
- Первая версия Dockerfile делал collectstatic на BUILD-стадии — SECRET_KEY недоступен при сборке. *Решение:* перенесён в CMD контейнера.

**Результат:** ✅ Dockerfile, docker-compose.yml, .dockerignore, requirements/{production.txt,base.txt}, config/settings/base.py, deployment_checklist skill.
---

### [2026-08-23 01:40] Задача: README refresh + чистка chat.html
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Финальная документационная зачистка.
**Что сделал:**
- [x] README: секции Docker-деплоя, демо-аккаунты, i18n, актуальные env-переменные, roadmap Phase 5 закрыт
- [x] chat.html: убран дублирующий CSRF-хук (глобальный уже в base.html), строки обёрнуты в translate
- [x] Коммит 08dc83e; remote origin=https://github.com/madsaomi/project.git — пуш НЕ делал (нужно решение владельца)

**Результат:** ✅ README.md, templates/messaging/chat.html. Тесты 47 passed.


---

### [2026-08-23 16:11] Задача: Тесты profiles/messaging + финальное i18n-покрытие
**Статус:** 🔄 IN_PROGRESS
**Агент:** ox-alpha (opencode)
**Контекст:** Пользователь просил продолжать. Оставались непротестированными напрямую builder/export_docx и send_message; не переведены form.html, builder/viewer.
**Что делаю:**
- [ ] Тесты: builder GET/POST, export_docx, chat_detail доступ, send_message HTMX
- [ ] i18n: обернуть internships/form.html, profiles/builder+viewer
- [ ] Каталоги + пересборка, тесты, коммит

**Прогресс:**
- ✅ [16:25] Тесты +8: profiles (builder create/save, export_docx, приватный viewer), messaging (detail доступ, HTMX send, пустое сообщение, чужой работодатель → redirect)
- ✅ 🐛 ТЕСТ ПОЙМАЛ БАГ: работодатель БЕЗ компании получал 500 в /messages/<pk>/ (request.user.company без hasattr-проверки в chat_detail и send_message). Исправлено redirect на главную
- ✅ i18n: обёрнуты form.html (заголовки/кнопки) и builder.html (все поля); каталоги 84 → 103 строки × {uz,en}
- ✅ conftest: UserFactory переведён на factory.django.Password + skip_postgeneration_save — 0 warnings
- ✅ Итог: 55 passed, 0 warnings, ruff clean

**Ошибки:**

**Решения:**

**Результат:** ✅ apps/{profiles/tests.py,messaging/tests.py,messaging/views.py}, templates/{internships/form.html,profiles/builder.html}, scripts/build_translations.py, locale/*, conftest.py.


---

