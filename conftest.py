import factory
import pytest

from apps.accounts.models import User
from apps.companies.models import Company
from apps.internships.models import Internship


@pytest.fixture(autouse=True)
def celery_eager(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@test.com')
    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    role = User.Role.STUDENT
    is_active = True
    accepted_terms = True


@pytest.fixture
def student_user(db):
    return User.objects.create_user(
        username='student_test',
        email='student@test.com',
        password='testpass123',
        role=User.Role.STUDENT,
    )


@pytest.fixture
def employer_user(db):
    user = User.objects.create_user(
        username='employer_test',
        email='employer@test.com',
        password='testpass123',
        role=User.Role.EMPLOYER,
    )
    Company.objects.create(
        user=user,
        name='Тестовая компания',
        verification_status=Company.VerificationStatus.VERIFIED,
    )
    return user


@pytest.fixture
def auth_student_client(student_user):
    from django.test import Client

    client = Client()
    client.force_login(student_user)
    return client


@pytest.fixture
def auth_employer_client(employer_user):
    from django.test import Client

    client = Client()
    client.force_login(employer_user)
    return client


@pytest.fixture
def internship_factory(db, employer_user):
    class InternshipFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Internship

        company = employer_user.company
        title = factory.Sequence(lambda n: f'Стажировка {n}')
        slug = factory.Sequence(lambda n: f'internship-{n}')
        description = 'Описание тестовой стажировки'
        internship_type = Internship.InternshipType.INTERNSHIP
        work_format = Internship.WorkFormat.REMOTE

    return InternshipFactory
