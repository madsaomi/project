import pytest
from django.test import Client
from django.urls import reverse

from apps.messaging.models import Conversation, Message
from conftest import UserFactory


@pytest.mark.django_db
def test_chat_detail_accessible_for_student_participant(
    auth_student_client, student_user, employer_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    auth_student_client.post(
        reverse('internships:apply', kwargs={'slug': internship.slug})
    )
    conversation = Conversation.objects.get(
        company=employer_user.company, student=student_user
    )

    response = auth_student_client.get(
        reverse('messaging:detail', kwargs={'pk': conversation.pk})
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_send_message_via_htmx(
    auth_student_client, student_user, employer_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    auth_student_client.post(
        reverse('internships:apply', kwargs={'slug': internship.slug})
    )
    conversation = Conversation.objects.get(
        company=employer_user.company, student=student_user
    )
    url = reverse('messaging:send', kwargs={'pk': conversation.pk})

    response = auth_student_client.post(url, {'content': 'Здравствуйте!'})

    assert response.status_code == 200
    message = Message.objects.get(conversation=conversation)
    assert message.content == 'Здравствуйте!'
    assert message.sender == student_user
    assert not message.is_read


@pytest.mark.django_db
def test_send_message_empty_content_redirects(
    auth_student_client, student_user, employer_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    auth_student_client.post(
        reverse('internships:apply', kwargs={'slug': internship.slug})
    )
    conversation = Conversation.objects.get(
        company=employer_user.company, student=student_user
    )
    url = reverse('messaging:send', kwargs={'pk': conversation.pk})

    response = auth_student_client.post(url, {'content': '   '})

    assert response.status_code == 302
    assert not Message.objects.filter(conversation=conversation).exists()


@pytest.mark.django_db
def test_other_company_cannot_read_conversation(student_user, internship_factory):
    outsider = UserFactory(role='employer')
    owner = UserFactory(role='employer')
    from apps.companies.models import Company

    other_company = Company.objects.create(user=owner, name='Чужая')
    internship = internship_factory(company=other_company)

    student_client = Client()
    student_client.force_login(student_user)
    student_client.post(reverse('internships:apply', kwargs={'slug': internship.slug}))
    conversation = Conversation.objects.get(
        company=other_company, student=student_user
    )

    outsider_client = Client()
    outsider_client.force_login(outsider)

    response = outsider_client.get(
        reverse('messaging:detail', kwargs={'pk': conversation.pk})
    )

    # Работодатель без отношения к чату уходит на главную, а не читает его
    assert response.status_code == 302


@pytest.mark.django_db
def test_send_message_htmx_returns_partial(
    auth_student_client, student_user, employer_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    auth_student_client.post(
        reverse('internships:apply', kwargs={'slug': internship.slug})
    )
    conversation = Conversation.objects.get(
        company=employer_user.company, student=student_user
    )
    url = reverse('messaging:send', kwargs={'pk': conversation.pk})

    response = auth_student_client.post(
        url, {'content': 'Через HTMX'}, HTTP_HX_REQUEST='true'
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_send_message_get_redirects_to_chat(
    auth_student_client, student_user, employer_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    auth_student_client.post(
        reverse('internships:apply', kwargs={'slug': internship.slug})
    )
    conversation = Conversation.objects.get(
        company=employer_user.company, student=student_user
    )
    url = reverse('messaging:send', kwargs={'pk': conversation.pk})

    response = auth_student_client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_task_skips_missing_participant(db):
    from apps.notifications.tasks import send_status_change_email

    result = send_status_change_email(999999, 'active')

    assert result is None
