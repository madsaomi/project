---
name: testing_guide
description: Как писать тесты в проекте StudCareer — pytest-django, factory_boy, структура тестов, примеры.
---

# Руководство по Тестированию (Testing Guide)

## 1. Стек тестирования

| Инструмент | Назначение |
|---|---|
| **pytest** | Основной тест-раннер |
| **pytest-django** | Интеграция с Django (управление БД, `rf`, `client`) |
| **factory_boy** | Создание тестовых объектов (вместо громоздких `setUp`) |
| **pytest-cov** | Покрытие кода |

Конфиг находится в `pyproject.toml`:
```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.development"
python_files = ["tests.py", "test_*.py", "*_tests.py"]
addopts = "--nomigrations --cov=. --cov-report=html"
```

---

## 2. Структура тестов

Тесты пишем **внутри каждого приложения**. Два подхода (оба допустимы):

### Вариант A: Один файл `tests.py` (для маленьких приложений)
```
apps/accounts/tests.py  ← уже есть, с тестами декораторов и миксинов
```

### Вариант B: Папка `tests/` (для больших приложений)
```
apps/internships/
└── tests/
    ├── __init__.py
    ├── test_models.py        # Тесты моделей
    ├── test_views.py         # Тесты представлений
    ├── test_signals.py       # Тесты сигналов (auto-create InternshipExperience)
    └── factories.py          # factory_boy фабрики
```

---

## 3. Фабрики (factory_boy)

### Базовая фабрика пользователей
```python
# apps/accounts/tests/factories.py (или conftest.py)
import factory
from apps.accounts.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@test.com')
    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    role = User.Role.STUDENT
    is_active = True


class EmployerFactory(UserFactory):
    role = User.Role.EMPLOYER


class AdminFactory(UserFactory):
    role = User.Role.ADMIN
    is_staff = True
    is_superuser = True
```

### Фабрика компании
```python
# apps/companies/tests/factories.py
import factory
from apps.companies.models import Company

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    user = factory.SubFactory('apps.accounts.tests.factories.EmployerFactory')
    name = factory.Sequence(lambda n: f'Компания {n}')
    verification_status = 'verified'
```

---

## 4. conftest.py (общие фикстуры)

Создайте `conftest.py` в корне проекта для общих фикстур:

```python
# conftest.py (в корне проекта)
import pytest
from apps.accounts.models import User


@pytest.fixture
def student_user(db):
    """Создаёт студента для тестов."""
    return User.objects.create_user(
        username='student_test',
        email='student@test.com',
        password='testpass123',
        role=User.Role.STUDENT,
    )


@pytest.fixture
def employer_user(db):
    """Создаёт работодателя для тестов."""
    return User.objects.create_user(
        username='employer_test',
        email='employer@test.com',
        password='testpass123',
        role=User.Role.EMPLOYER,
    )


@pytest.fixture
def auth_student_client(client, student_user):
    """Django test client залогиненный как студент."""
    client.force_login(student_user)
    return client


@pytest.fixture
def auth_employer_client(client, employer_user):
    """Django test client залогиненный как работодатель."""
    client.force_login(employer_user)
    return client
```

---

## 5. Примеры тестов

### Тест модели
```python
# apps/profiles/tests/test_models.py
import pytest
from apps.profiles.models import StudentProfile

@pytest.mark.django_db
def test_student_profile_created(student_user):
    profile = StudentProfile.objects.create(user=student_user, full_name='Иван Иванов')
    assert profile.full_name == 'Иван Иванов'
    assert profile.user == student_user
```

### Тест вьюхи (доступ)
```python
# apps/profiles/tests/test_views.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_builder_requires_login(client):
    url = reverse('profiles:builder')
    response = client.get(url)
    assert response.status_code == 302  # Редирект на login

@pytest.mark.django_db
def test_builder_accessible_for_logged_in(auth_student_client):
    url = reverse('profiles:builder')
    response = auth_student_client.get(url)
    assert response.status_code == 200
```

### Тест ролевого доступа (декораторы)
```python
# apps/internships/tests/test_views.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_create_internship_only_for_employer(auth_student_client, auth_employer_client):
    url = reverse('internships:create')

    # Студент → 404 (декоратор @employer_required)
    response = auth_student_client.get(url)
    assert response.status_code == 404

    # Работодатель → 200
    response = auth_employer_client.get(url)
    assert response.status_code == 200
```

### Тест HTMX partial response
```python
@pytest.mark.django_db
def test_catalog_returns_partial_for_htmx(auth_student_client):
    url = reverse('internships:catalog')

    # Обычный запрос → полная страница
    response = auth_student_client.get(url)
    assert 'catalog.html' in [t.name for t in response.templates]

    # HTMX-запрос → partial
    response = auth_student_client.get(url, HTTP_HX_REQUEST='true')
    assert '_list.html' in [t.name for t in response.templates]
```

### Тест object-level permission
```python
@pytest.mark.django_db
def test_employer_cannot_edit_others_internship(auth_employer_client, other_employer_internship):
    url = reverse('internships:edit', kwargs={'slug': other_employer_internship.slug})
    response = auth_employer_client.get(url)
    assert response.status_code == 404  # Чужая стажировка → 404
```

---

## 6. Запуск тестов

```powershell
# Все тесты
venv\Scripts\pytest

# Только конкретное приложение
venv\Scripts\pytest apps/profiles/

# Конкретный тест
venv\Scripts\pytest apps/accounts/tests.py::AccountsSecurityTestCase::test_student_required_decorator -v

# С подробным выводом
venv\Scripts\pytest -v

# Открыть HTML-отчет покрытия
start htmlcov/index.html
```

---

## 7. Чеклист: что тестировать в каждом приложении

| Что | Как | Пример |
|---|---|---|
| Модели: создание, связи | `@pytest.mark.django_db`, фабрики | Создать User → StudentProfile |
| Views: доступ | `client.get(url)` → проверить status_code | Анонимный → 302, залогиненный → 200 |
| Views: ролевой доступ | Тестировать с разными ролями | Студент → 200, работодатель → 404 |
| Views: HTMX partial | Заголовок `HTTP_HX_REQUEST='true'` | Проверить что возвращается partial |
| Views: object-level perm | Попытаться обратиться к чужому объекту | Чужая стажировка → 404 |
| Сигналы | Изменить статус → проверить побочный эффект | `completed` → InternshipExperience создан |
| Forms: валидация | Отправить невалидные данные | `form.is_valid() == False` |
