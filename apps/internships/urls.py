from django.urls import path

from . import views

app_name = 'internships'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('create/', views.create, name='create'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my/', views.my_internships, name='my_internships'),
    path('participants/<int:pk>/status/', views.update_participant_status, name='update_status'),
    path('<slug:slug>/edit/', views.edit, name='edit'),
    path('<slug:slug>/', views.detail, name='detail'),
    path('<slug:slug>/apply/', views.apply, name='apply'),
]
