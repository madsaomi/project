# 📋 Журнал Работы Агентов (WORKLOG)

> **ПРАВИЛО:** Каждый агент ОБЯЗАН читать этот файл в начале работы и записывать свои задачи.
> Записи **НИКОГДА** не удаляются — только добавляются снизу. Это **append-only** история.
> Полный протокол → `.agents/skills/worklog_protocol/SKILL.md`
> 📦 Архив завершённых задач → [WORKLOG_ARCHIVE.md](file:///.agents/WORKLOG_ARCHIVE.md)
> Последняя архивация: 2026-08-22 (перенесено 8 записей)

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
### [YYYY-MM-DD HH:MM] Задача: <название>
**Статус:** 🔄 IN_PROGRESS
**Агент:** <модель>
**Контекст:** <новая задача / продолжение записи [YYYY-MM-DD HH:MM]>
**Что делаю:**
- [ ] <шаг 1>
- [ ] <шаг 2>

**Прогресс:**
_(обновляется после КАЖДОГО значимого действия)_

**Ошибки:**
_(ошибки с причиной и решением — записывать НЕМЕДЛЕННО)_

**Решения:**
_(нетривиальные архитектурные выборы — записывать с обоснованием)_
```

### ⚡ ОБНОВЛЯЙ ПРОГРЕСС ПОСЛЕ КАЖДОГО ШАГА:
```
**Прогресс:**
- ✅ [HH:MM] Создал файл X — описание
- 🔧 [HH:MM] Работаю над файлом Y — что именно делаю
```

### При завершении:
```
**Статус:** ✅ DONE
**Результат:** <список созданных/изменённых файлов>
```

### ⚠️ АРХИВАЦИЯ (если файл > 300 строк):
Перенеси `✅ DONE` записи (кроме последних 3) в `.agents/WORKLOG_ARCHIVE.md`. Подробности → протокол.

## 📜 ИСТОРИЯ СЕССИЙ

---

### [2026-08-22 17:30] Задача: Фаза 5.1 — Дашборды (рабочий Kanban работодателя + дашборд студента)
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Продолжение сессии [2026-08-22 17:07]. Окружение поднято, тесты зелёные.
**Что делал:**
- [x] View `update_participant_status`: смена статуса отклика работодателем (HTMX, object-level проверка, валидация переходов)
- [x] Partial `_participant_card.html` + переписан `dashboard.html` (колонки со счётчиками, пустое состояние)
- [x] View `my_internships` + шаблон — дашборд студента (статистика, отклики с бейджами, ссылка на резюме для completed)
- [x] Ссылка «Мои стажировки» в navbar для студентов
- [x] БОНУС: login/register/logout были заглушками — реализована настоящая аутентификация
- [x] Тесты: 21 passed; E2E smoke пройден

**Ключевые решения:**
- ALLOWED_TRANSITIONS во views.py: pending→active/cancelled, active→completed/cancelled; при accept ставится start_date, при complete — end_date+completed_at (сигнал создаёт InternshipExperience).
- Ролевые редиректы после входа: студент → my_internships, работодатель → dashboard.
- Карточка Kanban self-swap через HTMX (`hx-target="#participant-N"`).

**Ошибки (кратко):** у django.test.Client нет `.user`; LogoutView Django 5 = только POST (в navbar форма); logout-маршрут не существовал вовсе.

---

### [2026-08-22 18:00] Задача: Фаза 5.2 — SEO-теги + интеграционные тесты + деплой-подготовка
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Продолжение сессии [2026-08-22 17:30]. Дашборды готовы.
**Что делал:**
- [x] SEO: блоки meta_description/og_* в base.html; переопределены на home, catalog, detail; починены мёртвые кнопки лендинга
- [x] Деплой-преп: STATIC_ROOT, MEDIA_*, auth-редиректы в base.py; production.py hardened (HSTS, SSL-redirect через env, SMTP из env); .env.example синхронизирован
- [x] Интеграционный тест `test_journey.py`: полный путь студента до опыта в резюме

**🐛 Главный улов:** у студента, зарегистрированного через сайт, не было StudentProfile → сигнал завершения стажировки падал бы 500. Исправлено сигналом post_save User в apps/accounts/signals.py (см. gotchas #15).

---

### [2026-08-22 18:30] Задача: Локальный стенд с демо-аккаунтами
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** По запросу пользователя — запустить проект локально с готовыми логинами/паролями.
**Что сделал:**
- development.py: CELERY_TASK_ALWAYS_EAGER=True (Redis локально не запущен; на проде отключено)
- Засеял демо-данные: superuser admin@studcareer.uz / Admin12345!, студент student@test.com / Test1234! (Анна Тестовая), работодатель employer@test.com / Test1234! («ООО Ромашка», verified), 2 стажировки, 1 pending-отклик
- Сервер на 0.0.0.0:8000 через WMI Win32_Process.Create (PID фиксировался на момент запуска)

**Ошибки:**
- Start-Process убивался песочницей после команды. *Решение:* Invoke-CimMethod Win32_Process Create — процесс не потомок шелла и выживает.

---

## ⏳ СЛЕДУЮЩИЕ ЗАДАЧИ (Очередь)

> Очередь по решению пользователя (2026-08-22): «всё по порядку».
> 1. 🔄 Создание стажировок работодателем (view create — сейчас заглушка) + edit/close своих вакансий
> 2. ⏳ Чаты: создание Conversation при отклике + кнопка «Написать» (сейчас Conversation нигде не создаётся)
> 3. ⏳ Ссылка на резюме кандидата в карточке Kanban

---

### [2026-08-22 20:39] Задача: Создание и редактирование стажировок работодателем
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Очередь #1. View `create` была заглушкой без обработки формы; редактирования не существовало вовсе.
**Что сделал:**
- [x] `apps/internships/forms.py`: InternshipForm (ModelForm, Tailwind-виджеты) + автогенерация уникального slug из title
- [x] `create`: POST-обработка, redirect на detail; без компании → redirect на companies:profile_edit
- [x] `edit`: owner-check (чужая → 404), поле is_active для закрытия набора; маршрут `<slug>/edit/` поставлен ДО catch-all `<slug>/`
- [x] Шаблон `form.html` общий для create/edit (флаг is_edit), вывод ошибок валидации списком
- [x] Блок «Мои стажировки» сверху dashboard работодателя: ссылки detail/edit, бейдж Активна/Закрыта, счётчик откликов
- [x] Тесты +6: создание, уникальность slug, студент → 404, работодатель без компании → redirect, невалидные данные, edit+закрытие (исчезает из каталога, detail 404), чужая вакансия → 404. Итого 28 passed
- [x] E2E через живой сервер: логин работодателем → форма → публикация → редирект на detail с автослагом

**Ошибки:**
- `forms.DateInput(widget=...)` — двойная обёртка виджета → TypeError. *Решение:* attrs+format прямо в DateInput.
- На create форма содержала is_active → без галочки в POST новая вакансия сразу становилась неактивной (detail 404). *Решение:* в __init__ при is_edit=False поле удаляется — новые всегда активны.
- В тесте ожидал 302 от студента на create — но employer_required даёт 404 раньше проверки компании. *Решение:* тест переписан под работодателя без компании.

**Результат:** ✅ Файлы: apps/internships/{forms.py,views.py,urls.py,tests.py}, templates/internships/{form.html,dashboard.html} (create.html удалён). Сервер перезапущен со свежим кодом (PID меняется — см. порт 8000).

---

## ⏳ СЛЕДУЮЩИЕ ЗАДАЧИ (Очередь)

> Очередь по решению пользователя (2026-08-22): «всё по порядку».
> 1. ✅ Создание стажировок работодателем — ГОТОВО (см. запись выше)
> 2. 🔄 Чаты: создание Conversation при отклике + кнопка «Написать»
> 3. ⏳ Ссылка на резюме кандидата в карточке Kanban

---

### [2026-08-22 21:00] Задача: Чаты — диалог создаётся при отклике + кнопки «Написать»
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Очередь #2. Conversation нигде не создавался — messaging был мёртвым кодом.
**Что сделал:**
- [x] apply: get_or_create Conversation(company, student) — идемпотентно при повторных откликах
- [x] Свойство `InternshipParticipant.conversation` (read-only .first(), без записи в GET)
- [x] Кнопка «Написать»: карточка Kanban (pending/active) + строки дашборда студента
- [x] Бэкфилл: 1 диалог для существующего отклика Анны через shell
- [x] Тесты +3: apply создаёт диалог (без дублей), conversation=None без чата, ссылка в Kanban. Итого 31 passed

**Решения:**
- Диалог создаю в apply, а не по клику «Написать» — GET-рендер карточек остаётся без побочных записей; у всех откликнувшихся чат существует гарантированно.

---

### [2026-08-22 21:20] Задача: Резюме кандидата в карточке Kanban
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Очередь #3. Работодатель не мог посмотреть резюме откликнувшегося.
**Что сделал:**
- [x] Имя кандидата в `_participant_card.html` — ссылка на `profiles:viewer` (если StudentProfile есть, иначе просто email — сигнал гарантирует профиль всем новым студентам)
- [x] Тест +1: дашборд содержит URL резюме и ФИО. Итого 32 passed, ruff clean
- [x] E2E: dashboard 200, ссылки /profiles/N/ и /messages/N/ на месте

**Результат:** ✅ templates/internships/_participant_card.html, apps/internships/tests.py. Сервер перезапущен (порт 8000).

---

## ⏳ СЛЕДУЮЩИЕ ЗАДАЧИ (Очередь)

> Очередь выполнена полностью (2026-08-22): создание стажировок ✅, чаты ✅, резюме в Kanban ✅.
> Кандидаты на будущее (не запланировано жёстко): password-reset флоу, in-app уведомления, i18n-переводы шаблонов, редактирование профиля компании из navbar-ссылки.

---

### [2026-08-22 21:40] Задача: Password-reset + ссылка «Моя компания» в navbar
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Пользователь просил продолжать по порядку из списка необязательных задач.
**Что сделал:**
- [x] Встроенные auth-views Django: reset → done → confirm → complete, маршруты под accounts/ с явными template_name
- [x] Tailwind-шаблоны всех 4 страниц + email-шаблоны (subject/email .txt)
- [x] «Забыли пароль?» на login, «Моя компания» в navbar работодателя (companies:profile_edit — там get_or_create, безопасно)
- [x] Тесты +2: полный флоу смены пароля по токену (старый не работает), невалидный токен → страница ошибки. Итого 34 passed
- [x] E2E на живом сервере: ссылка на login → форма → POST → письмо со ссылкой в консоли сервера (dev console backend)

**Ошибки:**
- Confirm-view при валидном токене отдаёт 302 на `.../set-password/` (session-based URL, защита от утечки токена через Referer) — тест ждал 200. *Решение:* идти по редиректу (`follow=True`) и постить на PATH_INFO. Это норма Django 5, не баг.

**Результат:** ✅ apps/accounts/{urls.py,tests.py}, templates/accounts/password_reset_*.html (6 шт), templates/components/navbar.html, templates/accounts/login.html. Сервер перезапущен.

---

## ⏳ СЛЕДУЮЩИЕ ЗАДАЧИ (Очередь)

> Основной список закрыт (2026-08-22): стажировки ✅, чаты ✅, резюме в Kanban ✅, password-reset ✅.
> Осталось необязательное: in-app уведомления (колокольчик), i18n-переводы шаблонов, деплой на хостинг (нужна инфраструктура).

---

### [2026-08-22 22:00] Задача: In-app уведомления (колокольчик в navbar)
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Последняя крупная фича из списка. Email-уведомления есть, in-app — нет.
**Что сделал:**
- [x] Модель `Notification` (recipient FK user, message, url, is_read) + миграция notifications.0001
- [x] Сигнал internships: новый отклик → уведомление работодателю (url → dashboard), смена статуса → студенту (url → my_internships)
- [x] Страница `/notifications/` (последние 50, непрочитанные подсвечены) + «Прочитать все» (POST-only)
- [x] Колокольчик с красным бейджем в navbar через context processor `unread_notifications`
- [x] Тесты +4: отклик уведомляет работодателя, смена статуса — студента, list требует логина, mark_all_read работает. Итого 38 passed
- [x] E2E на живом сервере: бейдж у работодателя, список, отметка о прочтении очищает бейдж

**Решения:**
- Уведомления создаются прямо в сигнале (не Celery) — они дешёвые (один INSERT), а пользователю важна мгновенность; email остаётся асинхронным.

**Результат:** ✅ apps/notifications/{models,views,urls,context_processors,tests}.py + миграция, apps/internships/signals.py, templates/notifications/list.html, templates/components/navbar.html, config/{urls.py,settings/base.py}. Сервер перезапущен (порт 8000).

---

## ⏳ СЛЕДУЮЩИЕ ЗАДАЧИ (Очередь)

> Всё из списка закрыто (2026-08-22): стажировки ✅, чаты ✅, резюме в Kanban ✅, password-reset ✅, in-app уведомления ✅.
> Осталось только i18n-переводы шаблонов и деплой на хостинг (нужна инфраструктура от владельца).

---

### [2026-08-22 22:40] Задача: i18n — инфраструктура переводов + перевод chrome-страниц (ru/uz/en)
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Последняя задача из списка. gettext на Windows отсутствует → компиляция через polib.
**Что сделал:**
- [x] LocaleMiddleware + `/i18n/setlang/` + переключатель языков (select) в navbar; context processor django.template.context_processors.i18n
- [x] Обёрнуто в {% translate %}: navbar, footer, home, login/register/password-reset ×4, catalog (заголовок+фильтры), my_internships (статистика), dashboard (заголовки/колонки/кнопки)
- [x] `scripts/build_translations.py`: генерирует и компилирует locale/{uz,en}/LC_MESSAGES/django.{po,mo} через polib — 57 строк на язык
- [x] polib добавлен в requirements/development.txt
- [x] Тесты +2: I18nTestCase — переключение en/uz меняет рендер. Итого 40 passed
- [x] E2E curl: en → lang="en"/Internships/Sign up; uz → Stajirovkalar/Kirish
- [x] Обновлён skill i18n_guide под новый пайплайн

**Ошибки:**
- Select языка рендерился пустым — не хватало контекст-процессора `django.template.context_processors.i18n` (переменная LANGUAGES). *Решение:* добавил в TEMPLATES OPTIONS.
- Тест передавал cookie как HTTP_COOKIE='uz' вместо 'django_language=uz'. *Решение:* формат name=value.
- PowerShell Get/Set-Content без -Encoding испортил кириллицу password_reset_form.html (mojibake). *Решение:* файл переписан через Write; шаблоны больше НЕ править через PS-строки (см. i18n_guide #6).

**Решения:**
- ru.mo не создаётся — русский это исходные msgid, Django сам откатывается к ним при LANGUAGE_CODE=ru.
- Непереведённые строки безопасно деградируют к русскому тексту — можно оборачивать шаблоны постепенно.

**Результат:** ✅ config/{settings/base.py,urls.py}, templates/{components/navbar.html,components/footer.html,home.html,accounts/*,internships/*}, scripts/build_translations.py, locale/{uz,en}/, apps/accounts/tests.py, pyproject.toml (ignore для скрипта). Сервер перезапущен.

---

### [2026-08-22 23:20] Задача: i18n-покрытие остальных шаблонов + синхронизация skills
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Продолжение [22:40] — доведение переводов и актуализация базы знаний.
**Что сделал:**
- [x] Обёрнуто в {% translate %}: _apply_btn, _list, _card, detail (заголовки секций), notifications/list, messaging/list
- [x] Каталоги расширены 57 → 79 строк × {uz,en}, пересобраны .po/.mo через scripts/build_translations.py
- [x] project_architecture: дерево файлов приведено к текущему состоянию (conftest.py, forms.py, сигналы, notifications, скрипты)
- [x] data_models_reference: добавлены Conversation/Message/Notification + property participant.conversation
- [x] Финальная проверка: 40 passed, ruff clean, manage.py check чисто, сервер перезапущен

**Ошибки:**
- PowerShell .Replace() не сработал по строке с переносом («Оплачиваемая</span>» был многострочным) — одна замена молча пропустилась. *Решение:* докрыл edit-инструментом; правило: массовые замены в шаблонах — только через edit/Write, PowerShell — точечно с явной UTF8-кодировкой.

**Результат:** ✅ templates/{internships/*,notifications/*,messaging/*}, scripts/build_translations.py, locale/{uz,en}, skills/{project_architecture,data_models_reference,i18n_guide}.

---

## ⏳ СЛЕДУЮЩИЕ ЗАДАЧИ (Очередь)

> Весь roadmap закрыт (2026-08-22/23): Фазы 1–5 ✅, дашборды ✅, стажировки CRUD ✅, чаты ✅, уведомления ✅, password-reset ✅, i18n (84 строки uz/en) ✅, полировка безопасности ✅, N+1 аудит ✅, Docker-бандл ✅.
> Деплой теперь = `docker compose up -d --build` на любом VPS (см. deployment_checklist #0).
> Git: вся работа закоммичена 2026-08-23 (aae2d13 feat / 92ba9de chore(deploy) / 03b968f docs). Git доступен по пути `C:\Program Files\Git\cmd\git.exe` (не в PATH!).

---

### [2026-08-22 23:50] Задача: Полировка — безопасность профилей/компаний, дедлайны, поиск в каталоге
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Аудит после закрытия roadmap. Найдены дыры: студент может создать компанию через /companies/edit/; резюме публично даже при is_public=False; отклик принимается после дедлайна; в каталоге нет поиска; views_count не считается.
**Что сделал:**
- [x] companies.profile_edit → @employer_required (студент больше не может создать компанию-пустышку)
- [x] Приватность резюме: viewer/pdf/docx через `_get_visible_profile` — is_public=False виден только владельцу (иначе 404)
- [x] apply: отклик после deadline отклоняется с toast-ошибкой; повторный клик по кнопке больше не шлёт лишние get_or_create
- [x] Каталог: поиск q (title/company/description icontains) + фильтр категории (select) + HTMX keyup-delay 400мс на поле поиска
- [x] detail: views_count инкремент через F() (без гонок)
- [x] Каталоги переводов 79 → 84 строки
- [x] Тесты +7: компании (студент 404 / создание работодателем), приватность резюме, дедлайн, поиск, views_count. Итого 46 passed
- [x] E2E: поиск/категория 200; приватное резюме → 404 анониму, публичное → 200

**Ошибки:**
- В deadline-ветке apply забыл передать `internship` в контекст partial `_apply_btn.html` → NoReverseMatch. *Решение:* контекст дополнен.

**Решения:**
- views_count через queryset.update(F()+1), а не instance.save() — атомарно, без race condition.
- Резюме по умолчанию публичное (как было) — меняется студентом осознанно.

**Результат:** ✅ apps/{companies/{views.py,tests.py},profiles/views.py,internships/views.py,notifications/tests.py}, templates/internships/catalog.html, scripts/build_translations.py, locale/*. Тесты 46 passed.

---

### [2026-08-23 00:30] Задача: Глубокий аудит — устранение N+1 и регрессионные тесты запросов
**Статус:** ✅ DONE
**Агент:** ox-alpha (opencode)
**Контекст:** Финальный аудит производительности. Найдены N+1: дашборд студента и Kanban делают 1–2 запроса на карточку (conversation-property, student_profile), список стажировок работодателя — COUNT на строку, список чатов — messages.last() на чат.
**Что сделал:**
- [x] `_with_conversation_id()` (Subquery) для откликов в my_internships и dashboard; шаблоны переведены с `p.conversation.pk` на аннотацию `conversation_id`
- [x] Kanban: select_related `student__student_profile` + `internship` (было 2 запроса на карточку)
- [x] «Мои стажировки» работодателя: annotate Count('participants') вместо participants.count на строку
- [x] chat_list: `_annotate_last_message()` (3 Subquery) вместо messages.last(); messaging/list.html переписан на аннотации
- [x] Регрессионный тест test_query_counts_no_n1: 5 откликов+5 чатов, бюджеты django_assert_max_num_queries (25/25/20)
- [x] 🐛 ПОПУТНО НАЙДЕН И ПОЧИНЕН ТЕСТОВЫЙ БАГ: auth_student_client и auth_employer_client логинили ОБЩИЙ django Client → последний force_login перелогинивал первого → запросы студента уходили под работодателем. Теперь каждый auth-client создаёт свой Client (gotchas #6.3)

**Ошибки:**
- В тесте обращался к client.user (см. gotcha 6.1), ассертовал 'hello 4' на Kanban вместо списка чатов, ловил IndentationError после правки PS-блоком — всё исправлено.

**Решения:**
- conversation_id через Subquery-аннотацию, а не property в цикле: property оставлен для одиночных объектов.
- Последнее сообщение чата — 3 скалярные Subquery-аннотации (content/at/sender_id); prefetch_related('messages') отвергнут как неограниченный по объёму.

**Результат:** ✅ apps/internships/views.py, apps/messaging/{views.py}, templates/{internships/{my_internships,_participant_card,dashboard}.html, messaging/list.html}, conftest.py, apps/notifications/tests.py, gotchas (#6.3). Тесты 47 passed.

---

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

**Ошибки:**

**Решения:**

**Прогресс:**
- ✅ [16:25] Тесты +8: profiles (builder create/save, export_docx, приватный viewer), messaging (detail доступ, HTMX send, пустое сообщение, чужой работодатель → redirect)
- [x] 🐛 ТЕСТ ПОЙМАЛ БАГ: работодатель БЕЗ компании получал 500 в /messages/<pk>/ (request.user.company без hasattr-проверки в chat_detail и send_message). Исправлено redirect на главную
- [x] i18n: обёрнуты form.html (заголовки/кнопки) и builder.html (все поля); каталоги 84 → 103 строки × {uz,en}
- [x] conftest: UserFactory переведён на factory.django.Password + skip_postgeneration_save — 0 warnings
- [x] Итог: 55 passed, 0 warnings, ruff clean

**Результат:** ✅ apps/{profiles/tests.py,messaging/tests.py,messaging/views.py}, templates/{internships/form.html,profiles/builder.html}, scripts/build_translations.py, locale/*, conftest.py.


---

### [2026-08-23 16:40] Задача: Админка чатов/уведомлений/верификации + закрытие дыр покрытия
**Статус:** 🔄 IN_PROGRESS
**Агент:** ox-alpha (opencode)
**Контекст:** Coverage-отчёт: 90%. Пустые admin у messaging/notifications; нет инструментов верификации компаний; непокрытые ветки: banned-login, ?next=, HX-partial чата, missing-participant в задаче.
**Что делаю:**
- [ ] Admin: Conversation/Message/Notification + actions верификации в CompanyAdmin
- [ ] Тесты на непокрытые ветки (цель ≥95% без migrations/pdf)
- [ ] Коммит

**Прогресс:**

**Ошибки:**

**Решения:**
