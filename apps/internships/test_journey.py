import pytest
from django.urls import reverse

from apps.internships.models import InternshipParticipant
from apps.profiles.models import InternshipExperience, StudentProfile


@pytest.mark.django_db
def test_full_student_journey(client, employer_user, internship_factory, django_user_model):
    """
    Интеграционный сценарий: регистрация студента → отклик → приём → завершение
    → опыт автоматически появляется в резюме.
    """
    # 1. Студент регистрируется (авто-логин, редирект в каталог)
    response = client.post(reverse('accounts:register'), {
        'email': 'journey@student.com',
        'password': 'strongpass123',
        'role': 'student',
    }, follow=True)
    assert response.status_code == 200
    student = django_user_model.objects.get(email='journey@student.com')
    assert client.session.get('_auth_user_id') == str(student.pk)

    # 2. В каталоге видна стажировка работодателя
    internship = internship_factory(company=employer_user.company)
    response = client.get(reverse('internships:catalog'))
    assert internship.title in response.content.decode()

    # 3. Отклик через HTMX-эндпоинт
    response = client.post(
        reverse('internships:apply', kwargs={'slug': internship.slug})
    )
    assert response.status_code == 200
    participant = InternshipParticipant.objects.get(
        internship=internship, student=student
    )
    assert participant.status == 'pending'

    # Повторный отклик не создаёт дубликат
    client.post(reverse('internships:apply', kwargs={'slug': internship.slug}))
    assert InternshipParticipant.objects.filter(
        internship=internship, student=student
    ).count() == 1

    # 4. Дашборд студента показывает отклик
    response = client.get(reverse('internships:my_internships'))
    assert internship.title in response.content.decode()
    assert 'На рассмотрении' in response.content.decode()

    # 5. Работодатель принимает отклик
    employer_client = client
    employer_client.logout()
    employer_client.force_login(employer_user)
    url = reverse('internships:update_status', kwargs={'pk': participant.pk})
    response = employer_client.post(url, {'status': 'active'})
    assert response.status_code == 200
    participant.refresh_from_db()
    assert participant.status == 'active'
    assert participant.start_date is not None
    assert not InternshipExperience.objects.filter(
        profile__user=student, internship=internship
    ).exists()

    # 6. Работодатель завершает стажировку → сигнал создаёт опыт в резюме
    response = employer_client.post(url, {'status': 'completed'})
    assert response.status_code == 200
    participant.refresh_from_db()
    assert participant.status == 'completed'
    assert participant.completed_at is not None

    experience = InternshipExperience.objects.get(
        profile__user=student, internship=internship
    )
    assert experience.company_name == employer_user.company.name
    assert experience.position == internship.title

    # 7. Опыт виден на странице резюме
    profile = StudentProfile.objects.get(user=student)
    response = client.get(reverse('profiles:viewer', kwargs={'pk': profile.pk}))
    assert response.status_code == 200
    assert employer_user.company.name in response.content.decode()

    # 8. Недопустимый повторный переход отклоняется
    response = employer_client.post(url, {'status': 'active'})
    participant.refresh_from_db()
    assert participant.status == 'completed'
