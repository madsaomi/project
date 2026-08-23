from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from apps.internships.models import InternshipParticipant
from apps.notifications.models import Notification
from apps.notifications.tasks import send_status_change_email
from apps.profiles.models import InternshipExperience


@receiver(post_save, sender=InternshipParticipant)
def handle_participant_status_change(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # Новый отклик → уведомить работодателя
        Notification.objects.create(
            recipient=instance.internship.company.user,
            message=(
                f'Новый отклик на стажировку «{instance.internship.title}» '
                f'от {instance.student.email}'
            ),
            url=reverse('internships:dashboard'),
        )
        return

    # Смена статуса → email + in-app уведомление студенту
    send_status_change_email.delay(instance.id, instance.status)
    Notification.objects.create(
        recipient=instance.student,
        message=(
            f'Статус вашего отклика на «{instance.internship.title}» изменён: '
            f'{instance.get_status_display()}'
        ),
        url=reverse('internships:my_internships'),
    )

    if instance.status == 'completed':
        InternshipExperience.objects.get_or_create(
            profile=instance.student.student_profile,
            internship=instance.internship,
            defaults={
                'company_name': instance.internship.company.name,
                'position': instance.position or instance.internship.title,
                'start_date': instance.start_date or instance.created_at.date(),
                'end_date': instance.end_date or timezone.now().date(),
            }
        )
