from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """У каждого студента должен быть StudentProfile — на него ссылается сигнал опыта."""
    if not created or instance.role != User.Role.STUDENT:
        return
    from apps.profiles.models import StudentProfile

    StudentProfile.objects.get_or_create(
        user=instance,
        defaults={'full_name': instance.username},
    )
