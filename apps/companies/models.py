from django.db import models
from django.db.models import CASCADE
from django.contrib.auth import get_user_model

User = get_user_model()

class Company(models.Model):
    """Профиль компании-работодателя"""
    user = models.OneToOneField(User, on_delete=CASCADE, related_name='company')
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    size = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('1-10','1-10'), ('11-50','11-50'),
            ('51-200','51-200'), ('200+','200+')
        ]
    )
    founded_year = models.PositiveIntegerField(null=True, blank=True)

    # Соцсети
    instagram_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # Верификация
    class VerificationStatus(models.TextChoices):
        PENDING = 'pending', 'На проверке'
        VERIFIED = 'verified', 'Верифицирована'
        REJECTED = 'rejected', 'Отклонена'

    verification_status = models.CharField(
        max_length=20, choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING
    )
    verified_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
