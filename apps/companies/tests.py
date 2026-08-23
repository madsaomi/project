import pytest
from django.test import Client
from django.urls import reverse

from apps.companies.models import Company
from conftest import UserFactory


@pytest.mark.django_db
def test_profile_edit_forbidden_for_student(student_user):
    client = Client()
    client.force_login(student_user)

    response = client.get(reverse('companies:profile_edit'))

    assert response.status_code == 404
    assert not Company.objects.exists()


@pytest.mark.django_db
def test_profile_edit_creates_company_for_employer():
    employer = UserFactory(role='employer')
    client = Client()
    client.force_login(employer)

    response = client.post(reverse('companies:profile_edit'), {
        'name': 'Наша компания',
        'description': 'Описание',
        'industry': 'IT',
        'website': 'https://example.uz',
    })

    company = Company.objects.get(user=employer)
    assert response.status_code == 302
    assert company.name == 'Наша компания'


@pytest.mark.django_db
def test_admin_verification_actions():
    from django.contrib.auth import get_user_model

    User = get_user_model()
    superuser = User.objects.create_superuser(
        email='root@studcareer.uz', username='root', password='Admin12345!',
        role='admin',
    )
    employer1 = UserFactory(role='employer')
    employer2 = UserFactory(role='employer')
    c1 = Company.objects.create(user=employer1, name='Первая')
    c2 = Company.objects.create(user=employer2, name='Вторая')

    admin_client = Client()
    admin_client.force_login(superuser)

    response = admin_client.post(
        reverse('admin:companies_company_changelist'),
        {'action': 'verify_companies', '_selected_action': [c1.pk, c2.pk]},
    )
    assert response.status_code == 302
    c1.refresh_from_db()
    c2.refresh_from_db()
    assert c1.verification_status == 'verified' and c1.verified_at is not None

    response = admin_client.post(
        reverse('admin:companies_company_changelist'),
        {'action': 'reject_companies', '_selected_action': [c2.pk]},
    )
    assert response.status_code == 302
    c2.refresh_from_db()
    assert c2.verification_status == 'rejected'
