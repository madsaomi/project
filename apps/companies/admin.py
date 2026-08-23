from django.contrib import admin
from django.utils import timezone

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'verification_status', 'industry', 'created_at')
    list_filter = ('verification_status', 'industry')
    search_fields = ('name', 'user__email')
    actions = ('verify_companies', 'reject_companies')

    @admin.action(description='Верифицировать выбранные компании')
    def verify_companies(self, request, queryset):
        updated = queryset.update(
            verification_status=Company.VerificationStatus.VERIFIED,
            verified_at=timezone.now(),
        )
        self.message_user(request, f'Верифицировано компаний: {updated}')

    @admin.action(description='Отклонить выбранные компании')
    def reject_companies(self, request, queryset):
        updated = queryset.update(verification_status=Company.VerificationStatus.REJECTED)
        self.message_user(request, f'Отклонено компаний: {updated}')
