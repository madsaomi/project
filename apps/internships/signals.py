from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.internships.models import InternshipParticipant
from apps.profiles.models import InternshipExperience
from apps.notifications.tasks import send_status_change_email

@receiver(post_save, sender=InternshipParticipant)
def handle_participant_status_change(sender, instance, **kwargs):
    # If this is not a new instance (status might have changed)
    if not kwargs.get('created', False):
        # Fire async email task
        send_status_change_email.delay(instance.id, instance.status)

    if instance.status == 'completed':
        InternshipExperience.objects.get_or_create(
            profile=instance.student.student_profile,
            internship=instance.internship,
            defaults={
                'company_name': instance.internship.company.name,
                'position': instance.position or instance.internship.title,
                'start_date': instance.start_date or instance.created_at.date(),
                'end_date': instance.end_date or instance.updated_at.date(),
            }
        )
