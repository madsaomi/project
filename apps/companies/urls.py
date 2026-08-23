from django.urls import path

from . import views

app_name = 'companies'

urlpatterns = [
    path('edit/', views.profile_edit, name='profile_edit'),
    path('<int:pk>/', views.profile_view, name='profile_view'),
]
