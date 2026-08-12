from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'verification_status', 'industry')
    list_filter = ('verification_status', 'industry')
    search_fields = ('name', 'user__email')
