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
