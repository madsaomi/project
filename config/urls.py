from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path('companies/', include('apps.companies.urls')),
    path('internships/', include('apps.internships.urls')),
    path('messages/', include('apps.messaging.urls')),
    path('', include('apps.core.urls')),
]
