from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Кастомный пользователь с ролями"""

    class Role(models.TextChoices):
        STUDENT = 'student', 'Студент'
        EMPLOYER = 'employer', 'Работодатель'
        ADMIN = 'admin', 'Администратор'

    role = models.CharField(max_length=20, choices=Role.choices)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    preferred_language = models.CharField(
        max_length=5,
        choices=[('ru','Русский'),('uz','Узбекский'),('en','Английский')],
        default='ru'
    )
    is_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    accepted_terms = models.BooleanField(default=False)  # ToS
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
