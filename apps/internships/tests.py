import pytest
from django.test import Client
from django.urls import reverse

from apps.companies.models import Company
from apps.internships.models import Internship, InternshipParticipant
from apps.profiles.models import InternshipExperience
from conftest import UserFactory


@pytest.mark.django_db
def test_catalog_view(client, internship_factory):
    internship_factory()
    url = reverse('internships:catalog')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_experience_signal(student_user, employer_user, internship_factory):
    # Setup
    internship = internship_factory(company=employer_user.company)
    participant = InternshipParticipant.objects.create(
        internship=internship,
        student=student_user,
        status='active'
    )

    # Assert no experience yet
    assert not InternshipExperience.objects.filter(profile=student_user.student_profile).exists()

    # Trigger signal
    participant.status = 'completed'
    participant.save()

    # Assert experience created
    assert InternshipExperience.objects.filter(profile=student_user.student_profile).exists()
    exp = InternshipExperience.objects.get(profile=student_user.student_profile)
    assert exp.company_name == internship.company.name


@pytest.mark.django_db
def test_update_status_accept(
    auth_employer_client, employer_user, student_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    participant = InternshipParticipant.objects.create(
        internship=internship, student=student_user, status='pending'
    )
    url = reverse('internships:update_status', kwargs={'pk': participant.pk})

    response = auth_employer_client.post(url, {'status': 'active'})

    assert response.status_code == 200
    participant.refresh_from_db()
    assert participant.status == 'active'
    assert participant.start_date is not None


@pytest.mark.django_db
def test_update_status_complete_creates_experience(
    auth_employer_client, employer_user, student_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    participant = InternshipParticipant.objects.create(
        internship=internship,
        student=student_user,
        status='active',
        start_date='2026-08-01',
    )
    url = reverse('internships:update_status', kwargs={'pk': participant.pk})

    response = auth_employer_client.post(url, {'status': 'completed'})

    assert response.status_code == 200
    participant.refresh_from_db()
    assert participant.status == 'completed'
    assert participant.end_date is not None
    assert InternshipExperience.objects.filter(
        profile=student_user.student_profile
    ).exists()


@pytest.mark.django_db
def test_update_status_invalid_transition(
    auth_employer_client, employer_user, student_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    participant = InternshipParticipant.objects.create(
        internship=internship, student=student_user, status='pending'
    )
    url = reverse('internships:update_status', kwargs={'pk': participant.pk})

    response = auth_employer_client.post(url, {'status': 'completed'})

    assert response.status_code == 200
    participant.refresh_from_db()
    assert participant.status == 'pending'


@pytest.mark.django_db
def test_update_status_forbidden_for_other_employer(
    auth_employer_client, student_user, internship_factory
):
    other_employer = UserFactory(role='employer')
    other_company = Company.objects.create(user=other_employer, name='Другая компания')
    internship = internship_factory(company=other_company)
    participant = InternshipParticipant.objects.create(
        internship=internship, student=student_user, status='pending'
    )
    url = reverse('internships:update_status', kwargs={'pk': participant.pk})

    response = auth_employer_client.post(url, {'status': 'active'})

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_status_forbidden_for_student(
    auth_student_client, student_user, internship_factory
):
    internship = internship_factory()
    participant = InternshipParticipant.objects.create(
        internship=internship, student=student_user, status='pending'
    )
    url = reverse('internships:update_status', kwargs={'pk': participant.pk})

    response = auth_student_client.post(url, {'status': 'active'})

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_status_get_not_allowed(
    auth_employer_client, employer_user, student_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    participant = InternshipParticipant.objects.create(
        internship=internship, student=student_user, status='pending'
    )
    url = reverse('internships:update_status', kwargs={'pk': participant.pk})

    response = auth_employer_client.get(url)

    assert response.status_code == 405


@pytest.mark.django_db
def test_my_internships_requires_login(client):
    url = reverse('internships:my_internships')
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_my_internships_shows_applications(
    auth_student_client, student_user, internship_factory
):
    internship = internship_factory()
    InternshipParticipant.objects.create(
        internship=internship, student=student_user, status='active'
    )
    url = reverse('internships:my_internships')

    response = auth_student_client.get(url)

    assert response.status_code == 200
    assert internship.title in response.content.decode()


@pytest.mark.django_db
def test_my_internships_forbidden_for_employer(auth_employer_client):
    url = reverse('internships:my_internships')

    response = auth_employer_client.get(url)

    assert response.status_code == 404


VALID_FORM_DATA = {
    'title': 'QA-стажёр',
    'internship_type': 'internship',
    'work_format': 'hybrid',
    'description': 'Тестирование веб-приложения.',
    'duration_months': 2,
    'location': 'Ташкент',
}


@pytest.mark.django_db
def test_create_internship_by_employer(auth_employer_client, employer_user):
    url = reverse('internships:create')

    response = auth_employer_client.post(url, VALID_FORM_DATA, follow=True)

    internship = Internship.objects.get(company=employer_user.company)
    assert response.status_code == 200
    assert internship.slug  # slug сгенерирован автоматически
    assert internship.is_active is True


@pytest.mark.django_db
def test_create_internship_slug_unique(auth_employer_client, employer_user):
    url = reverse('internships:create')
    data = {**VALID_FORM_DATA, 'title': 'Одна и та же вакансия'}

    auth_employer_client.post(url, data)
    auth_employer_client.post(url, data)

    slugs = list(
        Internship.objects.filter(company=employer_user.company)
        .values_list('slug', flat=True)
    )
    assert len(slugs) == 2
    assert len(set(slugs)) == 2


@pytest.mark.django_db
def test_create_internship_requires_company():
    employer_without_company = UserFactory(role='employer')
    client = Client()
    client.force_login(employer_without_company)

    response = client.post(reverse('internships:create'), VALID_FORM_DATA)

    assert response.status_code == 302
    assert response.url == reverse('companies:profile_edit')
    assert not Internship.objects.exists()


@pytest.mark.django_db
def test_create_internship_invalid_data(auth_employer_client):
    url = reverse('internships:create')

    response = auth_employer_client.post(url, {'title': ''})

    assert response.status_code == 200
    assert not Internship.objects.exists()


@pytest.mark.django_db
def test_edit_own_internship_and_close(auth_employer_client, employer_user, internship_factory):
    internship = internship_factory(company=employer_user.company)
    url = reverse('internships:edit', kwargs={'slug': internship.slug})

    response = auth_employer_client.get(url)
    assert response.status_code == 200

    response = auth_employer_client.post(
        url, {**VALID_FORM_DATA, 'is_active': 'on'}
    )
    assert response.status_code == 302
    internship.refresh_from_db()
    assert internship.title == 'QA-стажёр'
    assert internship.is_active is True

    # Закрыли набор — пропала из каталога и недоступна напрямую
    auth_employer_client.post(url, VALID_FORM_DATA)
    internship.refresh_from_db()
    assert internship.is_active is False
    catalog = auth_employer_client.get(reverse('internships:catalog'))
    assert internship.title not in catalog.content.decode()
    detail = auth_employer_client.get(
        reverse('internships:detail', kwargs={'slug': internship.slug})
    )
    assert detail.status_code == 404


@pytest.mark.django_db
def test_edit_other_employers_internship_404(
    auth_employer_client, employer_user, internship_factory
):
    other_employer = UserFactory(role='employer')
    other_company = Company.objects.create(user=other_employer, name='Чужая компания')
    internship = internship_factory(company=other_company)
    url = reverse('internships:edit', kwargs={'slug': internship.slug})

    response_get = auth_employer_client.get(url)
    response_post = auth_employer_client.post(url, VALID_FORM_DATA)

    assert response_get.status_code == 404
    assert response_post.status_code == 404


@pytest.mark.django_db
def test_apply_creates_conversation(auth_student_client, student_user, internship_factory):
    from apps.messaging.models import Conversation

    internship = internship_factory()
    url = reverse('internships:apply', kwargs={'slug': internship.slug})

    response = auth_student_client.post(url)

    assert response.status_code == 200
    conversation = Conversation.objects.get(
        company=internship.company, student=student_user
    )
    assert InternshipParticipant.objects.filter(
        internship=internship, student=student_user
    ).exists()

    # Повторный отклик не плодит диалоги
    auth_student_client.post(url)
    assert Conversation.objects.filter(
        company=internship.company, student=student_user
    ).count() == 1

    # Свойство participant.conversation находит диалог
    participant = InternshipParticipant.objects.get(
        internship=internship, student=student_user
    )
    assert participant.conversation == conversation


@pytest.mark.django_db
def test_conversation_none_without_chat(auth_student_client, student_user, internship_factory):
    internship = internship_factory()
    participant = InternshipParticipant.objects.create(
        internship=internship, student=student_user
    )

    assert participant.conversation is None


@pytest.mark.django_db
def test_kanban_card_shows_chat_link(
    auth_employer_client, employer_user, student_user, internship_factory
):
    from apps.messaging.models import Conversation

    internship = internship_factory(company=employer_user.company)
    InternshipParticipant.objects.create(
        internship=internship, student=student_user, status='pending'
    )
    conversation = Conversation.objects.create(
        company=employer_user.company, student=student_user
    )

    response = auth_employer_client.get(reverse('internships:dashboard'))

    assert response.status_code == 200
    assert reverse('messaging:detail', kwargs={'pk': conversation.pk}).encode() \
        in response.content


@pytest.mark.django_db
def test_kanban_card_links_to_resume(
    auth_employer_client, employer_user, student_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    profile = student_user.student_profile
    InternshipParticipant.objects.create(
        internship=internship, student=student_user, status='pending'
    )

    response = auth_employer_client.get(reverse('internships:dashboard'))

    assert response.status_code == 200
    assert reverse('profiles:viewer', kwargs={'pk': profile.pk}).encode() \
        in response.content
    assert profile.full_name in response.content.decode()
