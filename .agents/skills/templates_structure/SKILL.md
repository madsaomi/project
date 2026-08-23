---
name: templates_structure
description: Дерево шаблонов проекта, блоки base.html, паттерны HTMX partial-ответов и компоненты.
---

# Структура Шаблонов (Templates)

## 1. Дерево файлов (`templates/`)

> ⚠️ Обновляй при создании новых шаблонов.
> Последнее обновление: 2026-08-22 (Фаза 5.1 — дашборды)

```
templates/
├── base.html                   # Главный layout (Tailwind, Alpine, HTMX, Google Fonts)
├── home.html                   # Главная страница (лендинг)
│
├── components/
│   ├── navbar.html             # Навигация (роли, logout через POST-форму!)
│   ├── footer.html             # Подвал
│   └── toast.html              # Компонент уведомлений (Alpine.js события)
│
├── accounts/
│   ├── login.html              # Форма входа (+ блок error, ссылка «Забыли пароль?»)
│   ├── register.html           # Форма регистрации с выбором роли (+ блок error)
│   ├── password_reset_form.html    # Запрос сброса пароля
│   ├── password_reset_done.html    # «Письмо отправлено»
│   ├── password_reset_confirm.html # Новый пароль (или недействительная ссылка)
│   ├── password_reset_complete.html# «Пароль изменён»
│   ├── password_reset_email.txt    # Текст письма сброса
│   └── password_reset_subject.txt  # Тема письма
│
├── legal/
│   ├── terms_of_service.html   # ToS
│   └── privacy_policy.html     # Privacy Policy
│
├── profiles/
│   ├── builder.html            # Конструктор резюме (форма заполнения)
│   ├── viewer.html             # Просмотр резюме с кнопками экспорта
│   └── themes/
│       └── classic.html        # Тема резюме "Классика" (для viewer и PDF)
│
├── companies/
│   ├── edit.html               # Форма редактирования профиля компании
│   └── view.html               # Публичная страница компании
│
├── internships/
│   ├── catalog.html            # Каталог стажировок (полная страница)
│   ├── detail.html             # Страница стажировки
│   ├── form.html               # Общая форма создания/редактирования (is_edit)
│   ├── dashboard.html          # Kanban работодателя (+блок «Мои стажировки»)
│   ├── my_internships.html     # Дашборд студента (статистика + отклики)
│   ├── _list.html              # HTMX partial: список карточек каталога
│   ├── _card.html              # Карточка стажировки в каталоге
│   ├── _apply_btn.html         # Кнопка "Откликнуться" / "Вы откликнулись"
│   └── _participant_card.html  # Карточка кандидата в Kanban (HTMX self-swap)
│
└── messaging/
    ├── list.html               # Список чатов
    ├── chat.html               # Окно чата
    └── _message_feed.html      # HTMX partial: лента сообщений

└── notifications/
    └── list.html               # Список уведомлений (+«Прочитать все»)
```

---

## 2. Анатомия `base.html`

### Подключённые CDN (порядок важен!)
```html
<!-- 1. Tailwind CSS Play CDN + кастомный config -->
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: { primary: '#4F46E5', secondary: '#10B981', accent: '#F59E0B' },
        fontFamily: { sans: ['Inter', 'sans-serif'], serif: ['Merriweather', 'serif'] }
      }
    }
  }
</script>

<!-- 2. Alpine.js (defer — загружается после DOM) -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- 3. HTMX -->
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

<!-- 4. Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
```

### Ключевые блоки для наследования
```html
{% block title %}StudCareer{% endblock %}      <!-- Заголовок вкладки -->
{% block extra_head %}{% endblock %}           <!-- CSS, meta-теги -->
{% block content %}{% endblock %}              <!-- Основное содержимое -->
{% block extra_scripts %}{% endblock %}        <!-- JS в конце body -->
```

### Структура body
```html
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col antialiased">
  {% include 'components/navbar.html' %}     <!-- Навбар (ВСЕГДА) -->
  <main class="flex-grow">
    {% block content %}{% endblock %}
  </main>
  {% include 'components/footer.html' %}     <!-- Подвал (ВСЕГДА) -->
  {% include 'components/toast.html' %}      <!-- Toast (ВСЕГДА, скрыт по умолчанию) -->
  {% block extra_scripts %}{% endblock %}
</body>
```

> ⚠️ В `base.html` **нет** CSRF-заголовка для HTMX — его нужно добавить! См. `security_and_auth` #4 и `gotchas` #6.

---

## 3. Паттерны создания шаблонов

### Обычная страница (наследует base.html)
```html
{% extends 'base.html' %}

{% block title %}Каталог стажировок — StudCareer{% endblock %}

{% block content %}
<div class="max-w-7xl mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold text-slate-900">Каталог стажировок</h1>
  <!-- содержимое -->
</div>
{% endblock %}
```

### Partial-шаблон (для HTMX, НЕ наследует base.html)
```html
{# internships/_list.html — HTMX partial, возвращается только при HX-Request #}
{% for internship in internships %}
  {% include 'internships/_card.html' with internship=internship %}
{% empty %}
  <p class="text-slate-500 text-center py-8">Стажировки не найдены</p>
{% endfor %}
```

### Правила именования:
- Partial-шаблоны (для HTMX): **с `_` в начале** → `_list.html`, `_card.html`
- Полные страницы: **без `_`** → `catalog.html`, `detail.html`
- Это мгновенно говорит следующему разработчику, что шаблон частичный

---

## 4. HTMX Паттерны

### Обновление части страницы (Partial Response)
```python
# views.py
def my_view(request):
    # ... логика ...
    if request.headers.get('HX-Request'):
        return render(request, 'components/_my_partial.html', context)
    return render(request, 'my_full_page.html', context)
```

### Паттерн Toast-уведомления (Alpine.js + HTMX)
После успешного POST через HTMX, добавляй заголовок `HX-Trigger` в ответ:
```python
import json
from django.http import HttpResponse

response = HttpResponse(status=204)
response['HX-Trigger'] = json.dumps({
    'show-toast': {'message': 'Данные сохранены!', 'type': 'success'}
})
return response
```
Компонент `toast.html` автоматически поймает событие `show-toast.window` через Alpine.js.

### Паттерн: HTMX-фильтры (каталог)
```html
<!-- Фильтр меняет URL → HTMX обновляет только список -->
<select hx-get="{% url 'internships:catalog' %}"
        hx-target="#internship-list"
        hx-swap="innerHTML"
        hx-include="[name='work_format'], [name='is_paid']"
        name="work_format"
        class="rounded-lg border-slate-300">
  <option value="">Все форматы</option>
  <option value="remote">Удалённо</option>
  <option value="office">Офис</option>
</select>

<div id="internship-list">
  {% include 'internships/_list.html' %}
</div>
```

---

## 5. Компоненты (`components/`)

### `toast.html` — Уведомления
- Использует Alpine.js для показа/скрытия
- Слушает кастомное событие `show-toast` (триггерится через `HX-Trigger`)
- Автоматически скрывается через 3 секунды
- Типы: `success` (зелёный), `error` (красный), `info` (синий)

### `navbar.html` — Навигация
- Sticky (`fixed top-0`)
- Показывает разные ссылки в зависимости от `user.is_authenticated` и `user.role`
- Мобильное меню через Alpine.js

### `footer.html` — Подвал
- Ссылки на ToS, Privacy Policy
- Копирайт
