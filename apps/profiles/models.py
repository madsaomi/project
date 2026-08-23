from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE

User = get_user_model()

class StudentProfile(models.Model):
    """Анкета студента = Резюме"""
    user = models.OneToOneField(User, on_delete=CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='student_photos/', blank=True)
    headline = models.CharField(max_length=255, blank=True)  # "Python Developer Intern"
    about = models.TextField(blank=True)

    # Образование
    institution = models.CharField(max_length=255, blank=True)  # Вуз/колледж
    course = models.PositiveSmallIntegerField(null=True, blank=True)  # Курс
    specialty = models.CharField(max_length=255, blank=True)  # Специальность

    # Контакты и локация
    location = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Ссылки
    portfolio_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    behance_url = models.URLField(blank=True)

    # Настройки резюме
    resume_theme = models.CharField(
        max_length=20,
        choices=[('classic','Classic'),('modern','Modern'),('minimal','Minimal')],
        default='classic'
    )
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Skill(models.Model):
    """Навык студента"""
    profile = models.ForeignKey(StudentProfile, on_delete=CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(default=1)  # 1-5


class LanguageSkill(models.Model):
    """Язык студента"""
    profile = models.ForeignKey(StudentProfile, on_delete=CASCADE, related_name='language_skills')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)  # "A1", "B2", "Native"


class InternshipExperience(models.Model):
    """АВТОМАТИЧЕСКИ создаётся после завершения стажировки"""
    profile = models.ForeignKey(
        StudentProfile, on_delete=CASCADE, related_name='internship_experiences'
    )
    internship = models.OneToOneField(
        'internships.Internship', on_delete=CASCADE, related_name='experience_record'
    )
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
