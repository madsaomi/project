---
name: ui_ux_guidelines
description: Руководство по стилю, верстке, использованию Tailwind CSS, HTMX и Alpine.js.
---

# UI/UX Руководство StudCareer

## 1. Дизайн-система

### Цветовая палитра (кастомная, в tailwind.config)
Определена в `base.html` → `tailwind.config`:
```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: '#4F46E5',    // Indigo — основной акцент (кнопки, ссылки)
        secondary: '#10B981',  // Emerald — успех, подтверждения
        accent: '#F59E0B',     // Amber — предупреждения, featured-элементы
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],     // Основной текст
        serif: ['Merriweather', 'serif'],  // Заголовки резюме
      }
    }
  }
}
```

### Фоновые цвета и текст
| Назначение | Класс | Пример |
|---|---|---|
| Фон страницы | `bg-slate-50` | Устанавливается в `<body>` в base.html |
| Текст основной | `text-slate-800` | Устанавливается в `<body>` в base.html |
| Текст вторичный | `text-slate-500` | Описания, подписи |
| Карточки | `bg-white shadow-sm rounded-xl` | Карточки стажировок, профилей |
| Кнопки primary | `bg-primary text-white hover:bg-indigo-700` | CTA-кнопки |
| Кнопки secondary | `bg-slate-100 text-slate-700 hover:bg-slate-200` | Вторичные действия |
| Кнопки danger | `bg-red-50 text-red-600 hover:bg-red-100` | Отмена, удаление |

### Типографика
```html
<!-- Google Fonts (загружаются в base.html) -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
```

| Элемент | Классы |
|---|---|
| Заголовок страницы (h1) | `text-3xl font-bold text-slate-900` |
| Подзаголовок (h2) | `text-xl font-semibold text-slate-800` |
| Обычный текст | `text-base text-slate-700` |
| Мелкий текст / подписи | `text-sm text-slate-500` |
| Label формы | `text-sm font-medium text-slate-700` |

---

## 2. Tailwind CSS

### Подключение
Проект использует **Tailwind Play CDN** (для MVP-этапа):
```html
<script src="https://cdn.tailwindcss.com"></script>
```
> ⚠️ Play CDN — только для разработки. На продакшене (Фаза 5) нужна npm-сборка Tailwind.

### Правила
- **Запрещено** писать кастомный CSS без крайней необходимости. Все отступы, цвета и типографика — утилиты Tailwind.
- **Не используй** произвольные цвета (`bg-[#abc]`). Используй палитру из `tailwind.config` или стандартные Tailwind-цвета.
- Интерфейс должен выглядеть **«дорого» и минималистично**.

### Компоненты (часто используемые паттерны)

#### Карточка
```html
<div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6 hover:shadow-md transition-shadow">
  <h3 class="text-lg font-semibold text-slate-900">Заголовок</h3>
  <p class="mt-2 text-sm text-slate-500">Описание...</p>
</div>
```

#### Кнопка Primary
```html
<button class="inline-flex items-center gap-2 px-4 py-2 bg-primary text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50">
  Текст кнопки
</button>
```

#### Badge / Тег
```html
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700">
  Remote
</span>
```

#### Input поле формы
```html
<input type="text" class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-primary focus:ring-1 focus:ring-primary/50 outline-none transition-colors" placeholder="Введите...">
```

---

## 3. Адаптивность (Responsive)

Все страницы обязаны быть адаптивными. Breakpoints Tailwind:
| Breakpoint | Мин. ширина | Использование |
|---|---|---|
| `sm:` | 640px | Телефон (горизонтально) |
| `md:` | 768px | Планшет |
| `lg:` | 1024px | Десктоп |
| `xl:` | 1280px | Широкий десктоп |

Паттерн: **mobile-first**. Базовые стили — для мобильных, расширяем через `md:`, `lg:`.
```html
<!-- Пример: колонки -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <!-- карточки -->
</div>
```

---

## 4. HTMX

### Подключение
```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
```

### Принципы
- HTMX используется для **динамических обновлений** страницы без перезагрузки (AJAX).
- Формы и кнопки используют атрибуты `hx-post`, `hx-get`, `hx-target`, `hx-swap`.
- При написании views, возвращай **partial-шаблоны** (фрагменты HTML), если запрос пришёл через HTMX.

### Паттерн: определение HTMX-запроса в view
```python
def my_view(request):
    # ... логика ...
    if request.headers.get('HX-Request'):
        return render(request, 'app/_partial.html', context)
    return render(request, 'app/full_page.html', context)
```

### Паттерн: HTMX-кнопка с индикатором загрузки
```html
<button hx-post="{% url 'internships:apply' slug=internship.slug %}"
        hx-target="#apply-area"
        hx-swap="outerHTML"
        hx-indicator="#apply-spinner"
        class="bg-primary text-white px-4 py-2 rounded-lg">
  Откликнуться
</button>
<span id="apply-spinner" class="htmx-indicator">
  <svg class="animate-spin h-5 w-5 text-primary" ...></svg>
</span>
```

### CSRF для HTMX POST-запросов
Настроено глобально в `base.html`:
```html
<meta name="csrf-token" content="{{ csrf_token }}">
<script>
  document.body.addEventListener('htmx:configRequest', (e) => {
    e.detail.headers['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]').content;
  });
</script>
```
> ⚠️ **Если этого нет в base.html — HTMX POST будет возвращать 403!** Проверь `gotchas_and_known_issues` #6.

---

## 5. Alpine.js

### Подключение
```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

### Используется для:
- **Toast-уведомления** (`components/toast.html`) — работает на событиях `@show-toast.window`
- **Модальные окна** — `x-show`, `x-transition`
- **Переключатели** — dropdown-меню, сворачиваемые секции
- **Валидация форм** на клиенте

### Паттерн: Модальное окно
```html
<div x-data="{ open: false }">
  <button @click="open = true">Открыть</button>
  <div x-show="open" x-transition @click.away="open = false"
       class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
    <div class="bg-white rounded-xl p-6 max-w-md w-full shadow-2xl">
      <h3 class="text-lg font-semibold">Заголовок</h3>
      <button @click="open = false" class="mt-4 bg-primary text-white px-4 py-2 rounded-lg">Закрыть</button>
    </div>
  </div>
</div>
```

---

## 6. Иконки (Lucide)

### Подключение
```html
<script src="https://unpkg.com/lucide@latest"></script>
<script>lucide.createIcons();</script>
```

### Использование
```html
<i data-lucide="search" class="w-5 h-5 text-slate-400"></i>
<i data-lucide="briefcase" class="w-5 h-5 text-primary"></i>
<i data-lucide="map-pin" class="w-4 h-4 text-slate-500"></i>
```

> ⚠️ **Не подключайте** тяжеловесные иконочные шрифты (Font Awesome и т.п.). Только Lucide SVG.

---

## 7. Анимации и переходы

Все интерактивные элементы должны иметь плавные переходы:
```html
<!-- Кнопки -->
class="... transition-colors duration-150"

<!-- Карточки при наведении -->
class="... hover:shadow-md transition-shadow duration-200"

<!-- Появление элемента (Alpine) -->
x-transition:enter="transition ease-out duration-200"
x-transition:enter-start="opacity-0 scale-95"
x-transition:enter-end="opacity-100 scale-100"
```
