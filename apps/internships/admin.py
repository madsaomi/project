from django.contrib import admin

from .models import Category, Internship, InternshipParticipant, InternshipSkill


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'is_active', 'is_paid')
    list_filter = ('is_active', 'internship_type', 'work_format')
    search_fields = ('title', 'company__name')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(InternshipSkill)
admin.site.register(InternshipParticipant)
