from django.urls import path
from django.views.decorators.http import require_POST

from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('mark-read/', require_POST(views.mark_all_read), name='mark_all_read'),
]
