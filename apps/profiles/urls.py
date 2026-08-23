from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('builder/', views.builder, name='builder'),
    path('<int:pk>/', views.viewer, name='viewer'),
    path('<int:pk>/pdf/', views.export_pdf, name='export_pdf'),
    path('<int:pk>/docx/', views.export_docx, name='export_docx'),
]
