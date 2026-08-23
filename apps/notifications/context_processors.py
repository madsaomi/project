def unread_notifications(request):
    """Бейдж непрочитанных уведомлений для navbar."""
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}
