from django.db import models
from django.db.models import CASCADE, SET_NULL
from django.contrib.auth import get_user_model
from apps.companies.models import Company

User = get_user_model()

class Category(models.Model):
    """Категория стажировок"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)  # Lucide icon name
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=SET_NULL)


class Internship(models.Model):
    """Стажировка"""
    class InternshipType(models.TextChoices):
        INTERNSHIP = 'internship', 'Стажировка'
        PART_TIME = 'part_time', 'Подработка'
        PROJECT = 'project', 'Проектная работа'

    class WorkFormat(models.TextChoices):
        OFFICE = 'office', 'Офис'
        REMOTE = 'remote', 'Удалённо'
        HYBRID = 'hybrid', 'Гибрид'

    company = models.ForeignKey(Company, on_delete=CASCADE, related_name='internships')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    benefits = models.TextField(blank=True)

    internship_type = models.CharField(max_length=20, choices=InternshipType.choices)
    work_format = models.CharField(max_length=20, choices=WorkFormat.choices)
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True)

    # Оплата
    is_paid = models.BooleanField(default=False)
    salary_amount = models.PositiveIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=3, default='UZS')

    # Длительность
    duration_months = models.PositiveSmallIntegerField(default=1)

    location = models.CharField(max_length=255, blank=True)
    deadline = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InternshipSkill(models.Model):
    """Требуемые навыки для стажировки"""
    internship = models.ForeignKey(Internship, on_delete=CASCADE, related_name='required_skills')
    name = models.CharField(max_length=100)
    is_required = models.BooleanField(default=True)


class InternshipParticipant(models.Model):
    """Связь студента и стажировки (таймер)"""
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает подтверждения'
        ACTIVE = 'active', 'Активна'
        COMPLETED = 'completed', 'Завершена'
        CANCELLED = 'cancelled', 'Отменена'

    internship = models.ForeignKey(
        Internship, on_delete=CASCADE, related_name='participants'
    )
    student = models.ForeignKey(
        User, on_delete=CASCADE, related_name='internship_participations'
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=255, blank=True)  # Роль стажёра
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['internship', 'student']
