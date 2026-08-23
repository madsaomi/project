import pytest
from django.urls import reverse

from apps.internships.models import InternshipParticipant
from apps.notifications.models import Notification


@pytest.mark.django_db
def test_apply_notifies_employer(auth_student_client, employer_user, internship_factory):
    internship = internship_factory(company=employer_user.company)

    auth_student_client.post(reverse('internships:apply', kwargs={'slug': internship.slug}))

    notification = Notification.objects.get(recipient=employer_user)
    assert internship.title in notification.message
    assert notification.url == reverse('internships:dashboard')
    assert not notification.is_read


@pytest.mark.django_db
def test_status_change_notifies_student(
    auth_employer_client, employer_user, student_user, internship_factory
):
    internship = internship_factory(company=employer_user.company)
    participant = InternshipParticipant.objects.create(
        internship=internship, student=student_user, status='pending'
    )
    Notification.objects.all().delete()

    auth_employer_client.post(
        reverse('internships:update_status', kwargs={'pk': participant.pk}),
        {'status': 'active'},
    )

    notification = Notification.objects.get(recipient=student_user)
    assert 'Активна' in notification.message or 'активна' in notification.message
    assert notification.url == reverse('internships:my_internships')


@pytest.mark.django_db
def test_list_requires_login(client):
    response = client.get(reverse('notifications:list'))

    assert response.status_code == 302


@pytest.mark.django_db
def test_list_and_mark_all_read(student_user):
    from django.test import Client

    Notification.objects.create(recipient=student_user, message='Первое')
    Notification.objects.create(
        recipient=student_user, message='Второе', is_read=True
    )
    client = Client()
    client.force_login(student_user)

    response = client.get(reverse('notifications:list'))
    content = response.content.decode()
    assert response.status_code == 200
    assert 'Первое' in content
    assert 'Второе' in content

    response = client.post(reverse('notifications:mark_all_read'))

    assert response.status_code == 302
    assert not Notification.objects.filter(recipient=student_user, is_read=False).exists()


@pytest.mark.django_db
def test_apply_blocked_after_deadline(auth_student_client, internship_factory):
    from datetime import timedelta

    from django.utils import timezone as tz

    internship = internship_factory(deadline=tz.now().date() - timedelta(days=1))
    url = reverse('internships:apply', kwargs={'slug': internship.slug})

    response = auth_student_client.post(url)

    assert response.status_code == 200
    assert not InternshipParticipant.objects.filter(internship=internship).exists()


@pytest.mark.django_db
def test_catalog_search_by_title_and_company(
    auth_student_client, employer_user, internship_factory
):
    match = internship_factory(title='Django Backend Wizard', company=employer_user.company)
    miss = internship_factory(title='Художник-оформитель')

    response = auth_student_client.get(reverse('internships:catalog'), {'q': 'django'})

    content = response.content.decode()
    assert match.title in content
    assert miss.title not in content


@pytest.mark.django_db
def test_detail_increments_views_count(auth_student_client, internship_factory):
    internship = internship_factory()
    assert internship.views_count == 0

    auth_student_client.get(
        reverse('internships:detail', kwargs={'slug': internship.slug})
    )
    auth_student_client.get(
        reverse('internships:detail', kwargs={'slug': internship.slug})
    )

    internship.refresh_from_db()
    assert internship.views_count == 2


@pytest.mark.django_db
def test_private_resume_hidden_from_others(student_user, client):
    from django.test import Client


    profile = student_user.student_profile
    profile.is_public = False
    profile.save()

    # Аноним и чужой пользователь → 404
    assert client.get(f'/profiles/{profile.pk}/').status_code == 404

    other = Client()
    other.force_login(student_user)
    assert other.get(f'/profiles/{profile.pk}/').status_code == 200


@pytest.mark.django_db
def test_query_counts_no_n1(
    auth_student_client,
    auth_employer_client,
    employer_user,
    student_user,
    internship_factory,
    django_assert_max_num_queries,
):
    from apps.messaging.models import Conversation, Message

    for i in range(5):
        internship = internship_factory(
            company=employer_user.company,
            title=f'Vacancy {i}',
            slug=f'vacancy-{i}',
        )
        response = auth_student_client.post(
            reverse('internships:apply', kwargs={'slug': internship.slug})
        )
        if response.status_code != 200:
            pytest.fail(f'apply {internship.slug} -> {response.status_code}')
        conversation = Conversation.objects.get(
            company=employer_user.company, student=student_user
        )
        Message.objects.create(
            conversation=conversation,
            sender=student_user,
            content=f'hello {i}',
        )

    with django_assert_max_num_queries(25):
        response = auth_student_client.get(reverse('internships:my_internships'))
    assert response.status_code == 200

    with django_assert_max_num_queries(25):
        response = auth_employer_client.get(reverse('internships:dashboard'))
    assert response.status_code == 200
    assert 'Vacancy 4' in response.content.decode()
    assert 'Написать' in response.content.decode()

    with django_assert_max_num_queries(20):
        response = auth_employer_client.get(reverse('messaging:list'))
    assert response.status_code == 200
    assert 'hello 4' in response.content.decode()
