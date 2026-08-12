from django.contrib import admin
from .models import StudentProfile, Skill, LanguageSkill, InternshipExperience

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'institution', 'course', 'is_public')
    search_fields = ('full_name', 'user__email')

admin.site.register(Skill)
admin.site.register(LanguageSkill)
admin.site.register(InternshipExperience)
