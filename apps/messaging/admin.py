from django.contrib import admin

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'content', 'is_read', 'created_at')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'company', 'created_at', 'updated_at')
    search_fields = ('student__email', 'company__name')
    list_filter = ('company__verification_status',)
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'short_content', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('content', 'sender__email')

    @admin.display(description='Сообщение')
    def short_content(self, obj):
        return obj.content[:60]
