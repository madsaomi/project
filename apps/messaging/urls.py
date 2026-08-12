from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.chat_list, name='list'),
    path('<int:pk>/', views.chat_detail, name='detail'),
    path('<int:pk>/send/', views.send_message, name='send'),
]
