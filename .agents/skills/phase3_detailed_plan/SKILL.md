---
name: phase3_detailed_plan
description: Детальный технический план реализации Фазы 3 — Каталог стажировок, создание стажировок работодателем, отклики студентов и Kanban-доска.
---

# Фаза 3: Стажировки и Отклики — Детальный план

> **Цель:** Связать студентов и работодателей. Студент может найти стажировку и откликнуться, работодатель — управлять кандидатами.

---

## Что уже готово (задел из Фазы 2)
- Модели `Internship`, `Category`, `InternshipSkill`, `InternshipParticipant` полностью описаны и мигрированы в `apps/internships/models.py`.
- Базовый `InternshipsConfig` прописан в `INSTALLED_APPS`.
- Панель Admin уже настроена (`admin.py`).

---

## Шаг 1: Каталог стажировок (для всех)

### URL: `/internships/`
**View (`apps/internships/views.py`):**
```python
def catalog(request):
    qs = Internship.objects.filter(is_active=True).select_related('company', 'category')
    # Фильтры через GET-параметры (HTMX обновляет только список)
    if work_format := request.GET.get('work_format'):
        qs = qs.filter(work_format=work_format)
    if is_paid := request.GET.get('is_paid'):
        qs = qs.filter(is_paid=is_paid == 'true')
    if request.headers.get('HX-Request'):
        return render(request, 'internships/_list.html', {'internships': qs})
    return render(request, 'internships/catalog.html', {'internships': qs})
```

**Шаблоны:**
- `internships/catalog.html` — полная страница с фильтрами (sidebar) и списком.
- `internships/_list.html` — HTMX partial: только карточки стажировок.
- `internships/_card.html` — одна карточка стажировки.

---

## Шаг 2: Страница стажировки + Отклик

### URL: `/internships/<slug>/`
- Показывает полное описание стажировки.
- Кнопка "Откликнуться" для студентов — HTMX POST, не перезагружает страницу.

### URL: `/internships/<slug>/apply/` (POST, student only)
```python
@login_required
def apply(request, slug):
    internship = get_object_or_404(Internship, slug=slug, is_active=True)
    participant, created = InternshipParticipant.objects.get_or_create(
        internship=internship, student=request.user
    )
    # Вернуть HTMX partial с новой кнопкой "Вы уже откликнулись"
    response = render(request, 'internships/_apply_btn.html', {'applied': True})
    response['HX-Trigger'] = json.dumps({'show-toast': {'message': 'Отклик отправлен!', 'type': 'success'}})
    return response
```

---

## Шаг 3: Создание стажировки (employer only)

### URL: `/internships/create/`
- Доступ только для `role='employer'`.
- Форма с полями из модели `Internship`.
- После создания — редирект на страницу стажировки.

---

## Шаг 4: Kanban-доска (dashboard employer)

### URL: `/dashboard/`
- Показывает все стажировки компании и кандидатов по колонкам: **Pending → Active → Completed**.
- Смена статуса через HTMX PATCH/POST (перетаскивание карточки или кнопки).

### Автоматизация (критичная бизнес-логика!):
При переводе `InternshipParticipant.status` в `'completed'` — **автоматически** создать `InternshipExperience`:
```python
# В signals.py или в service-функции
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=InternshipParticipant)
def create_experience_on_completion(sender, instance, **kwargs):
    if instance.status == 'completed':
        InternshipExperience.objects.get_or_create(
            profile=instance.student.student_profile,
            internship=instance.internship,
            defaults={
                'company_name': instance.internship.company.name,
                'position': instance.position or instance.internship.title,
                'start_date': instance.start_date,
                'end_date': instance.end_date,
            }
        )
```

---

## Чеклист задач Фазы 3
- `[ ]` `apps/internships/views.py` — catalog, detail, apply, create, dashboard.
- `[ ]` `apps/internships/urls.py` — все маршруты.
- `[ ]` Шаблоны: `catalog.html`, `detail.html`, `create.html`, `dashboard.html`.
- `[ ]` Partial-шаблоны: `_list.html`, `_card.html`, `_apply_btn.html`.
- `[ ]` Сигнал/сервис автоматического создания `InternshipExperience`.
- `[ ]` Подключить `internships.urls` в `config/urls.py`.
- `[ ]` Обновить Navbar: добавить ссылку "Стажировки".
- `[ ]` Тесты для логики отклика и автоматического создания опыта.
