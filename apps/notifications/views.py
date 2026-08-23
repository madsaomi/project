from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def notification_list(request):
    """Список уведомлений пользователя."""
    items = request.user.notifications.all()[:50]
    return render(request, 'notifications/list.html', {'items': items})


@login_required
def mark_all_read(request):
    """Отметить все уведомления прочитанными."""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('notifications:list')
