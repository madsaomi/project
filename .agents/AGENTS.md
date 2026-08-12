# StudCareer — Платформа Стажировок

**Краткая суть:** Это не HH.ru, а трекер стажировок. Студент без опыта проходит стажировку, и она автоматически добавляется ему в профиль/резюме.

> ## 🚨 ПЕРВЫЙ ШАГ ДЛЯ ЛЮБОГО АГЕНТА
> **Прочитай [`WORKLOG.md`](file:///c:/Users/~/Desktop/New%20folder/.agents/WORKLOG.md) перед любым действием!**
> Там история всех предыдущих сессий, незавершённые задачи и очередь следующих.
> Протокол ведения журнала → [`worklog_protocol`](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/worklog_protocol/SKILL.md)
>
> ### 🔴 ОБЯЗАТЕЛЬНЫЕ ТРЕБОВАНИЯ (нарушение = потеря работы):
> 1. **Чекпоинты** — обновляй `**Прогресс:**` после КАЖДОГО значимого действия. Без этого при обрыве вся работа потеряна.
> 2. **Ошибки** — записывай ВСЕ ошибки в `**Ошибки:**` с причиной и решением. Иначе следующий агент наступит на те же грабли.
> 3. **Решения** — фиксируй нетривиальные архитектурные выборы в `**Решения:**`. Иначе следующий агент переделает без причины.
> 4. **Архивация** — если WORKLOG.md > 300 строк, перенеси `✅ DONE` записи в `WORKLOG_ARCHIVE.md` (см. протокол).

---

## ⚡ Quick Start (первые 5 минут нового агента)

**Шаг 1.** Прочитай [`WORKLOG.md`](file:///c:/Users/~/Desktop/New%20folder/.agents/WORKLOG.md) — найди `🔄 IN_PROGRESS` или `⏳ PENDING`.
**Шаг 2.** Прочитай нужные скиллы (см. таблицу ниже — выбери по задаче).
**Шаг 3.** Создай свою запись в WORKLOG **ДО** первого изменения в коде.
**Шаг 4.** Работай, обновляй `**Прогресс:**` после каждого файла.

### Какие скиллы читать в зависимости от задачи:

| Задача | Обязательно прочитай |
|---|---|
| Любая задача | `WORKLOG.md` → `worklog_protocol` |
| Новые views/urls | `api_and_urls` → `coding_conventions` → `security_and_auth` |
| Работа с моделями | `data_models_reference` → `gotchas_and_known_issues` |
| Новые шаблоны | `templates_structure` → `ui_ux_guidelines` |
| Фаза 3 (стажировки) | `phase3_detailed_plan` → `business_logic` |
| Тесты | `testing_guide` |
| Деплой | `deployment_checklist` |
| Фоновые задачи | `background_tasks` |
| Первый запуск проекта | `development_workflow` |

---

## Дополнительный контекст (Skills)
Для детальной информации, пожалуйста, обращайтесь к соответствующим навыкам (skills) в папке `.agents/skills/`:
- **[project_architecture](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/project_architecture/SKILL.md)**: Структура проекта, дерево файлов, ER-диаграмма моделей.
- **[ui_ux_guidelines](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/ui_ux_guidelines/SKILL.md)**: Правила использования Tailwind CSS, Alpine.js и HTMX.
- **[development_workflow](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/development_workflow/SKILL.md)**: Запуск проекта с нуля, миграции, тесты, Django shell.
- **[business_logic](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/business_logic/SKILL.md)**: Жизненный цикл стажировок, роли, автоматическое создание опыта.
- **[background_tasks](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/background_tasks/SKILL.md)**: Celery, Redis, правила написания async-задач.
- **[security_and_auth](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/security_and_auth/SKILL.md)**: Готовые декораторы ролей, object-level permissions, CSRF/XSS.
- **[data_models_reference](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/data_models_reference/SKILL.md)**: Полная шпаргалка по всем полям всех моделей.
- **[templates_structure](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/templates_structure/SKILL.md)**: Дерево шаблонов, блоки, паттерны HTMX partial-ответов.
- **[api_and_urls](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/api_and_urls/SKILL.md)**: Полная карта всех URL-маршрутов проекта.
- **[gotchas_and_known_issues](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/gotchas_and_known_issues/SKILL.md)**: ⚠️ Ловушки, критические предупреждения, частые ошибки.
- **[testing_guide](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/testing_guide/SKILL.md)**: pytest, factory_boy, структура тестов и примеры.
- **[phase3_detailed_plan](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/phase3_detailed_plan/SKILL.md)**: 🚧 Детальный технический план Фазы 3 с чеклистом.
- **[media_and_static](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/media_and_static/SKILL.md)**: MEDIA_ROOT, MEDIA_URL, Pillow, collectstatic.
- **[i18n_guide](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/i18n_guide/SKILL.md)**: makemessages, compilemessages, переводы в шаблонах.
- **[coding_conventions](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/coding_conventions/SKILL.md)**: Именование, структура view, чеклист нового приложения.
- **[deployment_checklist](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/deployment_checklist/SKILL.md)**: Nginx, Gunicorn, .env, collectstatic перед деплоем.
- **[worklog_protocol](file:///c:/Users/~/Desktop/New%20folder/.agents/skills/worklog_protocol/SKILL.md)**: 🔁 Протокол ведения журнала работы агентов (обязателен к прочтению).

---

## 🗺 Карта Проекта (Roadmap & History)

### ✅ Что уже сделано (Фазы 1 и 2)
1. **Базовый каркас (Фаза 1):**
   - Настроено виртуальное окружение и установлены зависимости (WeasyPrint, Celery, HTMX и др.).
   - Проект разбит на изолированные файлы настроек (base, development, production).
   - Подключены i18n, линтеры (Ruff), pytest и pre-commit.
   - Написана кастомная модель `accounts.User` с авторизацией по email и ролями.
   - Сверстаны базовые шаблоны (`base.html`, `navbar.html`, `footer.html`, `toast.html`) с Tailwind CSS, Alpine.js и HTMX.
   - Написаны базовые представления для Входа и Регистрации, ToS, Privacy Policy.

2. **Профили и Компании (Фаза 2):**
   - Созданы приложения `profiles`, `companies` и `internships`. Описаны и мигрированы модели.
   - Модели подключены к встроенной панели администратора Django.
   - Разработан **Конструктор резюме** (`profiles/builder/`) и форма просмотра резюме (`profiles/viewer/`).
   - Настроен экспорт резюме "на лету" в форматы **PDF** (через WeasyPrint) и **DOCX** (через python-docx).
   - Созданы представления и шаблоны для редактирования и просмотра профиля компании.

### 🔄 Что делаем сейчас (Текущий статус)
- Фаза 2 завершена. Мы находимся на границе между профилями и функционалом стажировок. Базовые модели для стажировок уже готовы, но бизнес-логика еще не описана.
- Ожидаем старт **Фазы 3**, которая объединит студентов и работодателей.

### 🚀 Планы на будущее (Что будет дальше)
3. **Фаза 3: Стажировки и Отклики (Internships & Applications)**
   - Каталог стажировок с поиском и фильтрами (реализация без перезагрузки страницы через HTMX).
   - Интерфейс работодателя для создания новых стажировок.
   - Процесс отклика на стажировку и доска кандидатов (Канбан/Списки) для изменения статуса откликов.
4. **Фаза 4: Уведомления и Сообщения (Messaging & Notifications)**
   - Базовый чат между студентом и работодателем.
   - Фоновые задачи (Celery/Redis) для отправки email и in-app уведомлений.
5. **Фаза 5: Аналитика и Полировка (Analytics & Polish)**
   - Дашборды для студентов и работодателей.
   - SEO-оптимизация (Title tags, meta descriptions).
   - Финальные интеграционные тесты и подготовка к деплою на продакшен.

---

## Правила для Агентов (System Prompt Additions)
1. **Не читай весь проект целиком!** Используй поиск (grep_search) для навигации, чтобы не тратить токены впустую.
2. Ищите приложения в папке `apps/` (например, `apps/profiles/models.py`).
3. Используйте TailwindCSS классы в шаблонах. Всегда делайте UI современным и привлекательным.
4. Используйте HTMX для интерактивности вместо написания сырого JS.
5. В качестве иконок используйте SVG-иконки Lucide.
6. **Обновляй `project_architecture`** при создании новых приложений или значимых файлов (дерево файлов должно быть актуальным).
7. **Нерешённые ошибки (`⚠️`) из WORKLOG** → переноси в `gotchas_and_known_issues` при завершении задачи.
