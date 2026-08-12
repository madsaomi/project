import pytest
from django.urls import reverse
from apps.internships.models import Internship, InternshipParticipant
from apps.profiles.models import InternshipExperience

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
