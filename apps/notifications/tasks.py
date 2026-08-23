from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
)
def send_status_change_email(self, participant_id, new_status):
    """
    Уведомить студента об изменении статуса отклика.
    Вызывается: при смене InternshipParticipant.status.
    """
    from django.core.mail import send_mail

    from apps.internships.models import InternshipParticipant

    try:
        participant = InternshipParticipant.objects.select_related(
            'student', 'internship__company'
        ).get(id=participant_id)
    except InternshipParticipant.DoesNotExist:
        logger.warning(f"Participant {participant_id} not found, skipping email")
        return

    # In production, use template rendering for emails
    send_mail(
        subject=f'Статус вашего отклика изменён: {new_status}',
        message=(
            f'Ваш отклик на "{participant.internship.title}" '
            f'теперь имеет статус: {new_status}.'
        ),
        from_email='noreply@studcareer.uz',
        recipient_list=[participant.student.email],
    )
    logger.info(f"Email sent to {participant.student.email} for status={new_status}")
