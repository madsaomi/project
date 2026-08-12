from django.urls import path
from . import views

app_name = 'internships'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('create/', views.create, name='create'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<slug:slug>/', views.detail, name='detail'),
    path('<slug:slug>/apply/', views.apply, name='apply'),
]
