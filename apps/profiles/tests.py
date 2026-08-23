import pytest
from django.test import Client
from django.urls import reverse

from apps.profiles.models import StudentProfile
from conftest import UserFactory


@pytest.mark.django_db
def test_builder_creates_profile_on_first_visit():
    user = UserFactory(role='student')
    client = Client()
    client.force_login(user)

    response = client.get(reverse('profiles:builder'))

    assert response.status_code == 200
    assert StudentProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_builder_saves_fields(student_user):
    profile = student_user.student_profile
    client = Client()
    client.force_login(student_user)

    response = client.post(reverse('profiles:builder'), {
        'full_name': 'Анна Тестовая',
        'headline': 'Junior Python Developer',
        'about': 'Ищу первую стажировку',
        'institution': 'ТГТУ',
        'specialty': 'Компьютерная инженерия',
    })

    assert response.status_code == 302
    profile.refresh_from_db()
    assert profile.headline == 'Junior Python Developer'
    assert profile.institution == 'ТГТУ'


@pytest.mark.django_db
def test_export_docx_returns_document(auth_student_client, student_user):
    profile = student_user.student_profile
    profile.full_name = 'Анна Тестовая'
    profile.save()
    url = reverse('profiles:export_docx', kwargs={'pk': profile.pk})

    response = auth_student_client.get(url)

    assert response.status_code == 200
    assert response['Content-Type'] == (
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    assert 'attachment' in response['Content-Disposition']


@pytest.mark.django_db
def test_viewer_shows_owner_for_private_profile(student_user):
    profile = student_user.student_profile
    profile.is_public = False
    profile.save()
    client = Client()
    client.force_login(student_user)
    url = reverse('profiles:viewer', kwargs={'pk': profile.pk})

    response = client.get(url)

    assert response.status_code == 200
