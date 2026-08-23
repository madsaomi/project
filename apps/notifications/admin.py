from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('message', 'recipient__email')
    readonly_fields = ('recipient', 'message', 'url', 'created_at')

    def has_add_permission(self, request):
        return False
