from django import forms
from django.utils.text import slugify

from .models import Internship

TAILWIND_INPUT = (
    'mt-1 block w-full rounded-md border-gray-300 shadow-sm '
    'focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
)
TAILWIND_CHECKBOX = 'rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'


class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = [
            'title', 'category', 'internship_type', 'work_format',
            'description', 'requirements', 'responsibilities', 'benefits',
            'is_paid', 'salary_amount', 'duration_months',
            'location', 'deadline', 'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'category': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'internship_type': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'work_format': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': TAILWIND_INPUT}),
            'requirements': forms.Textarea(attrs={'rows': 3, 'class': TAILWIND_INPUT}),
            'responsibilities': forms.Textarea(attrs={'rows': 3, 'class': TAILWIND_INPUT}),
            'benefits': forms.Textarea(attrs={'rows': 2, 'class': TAILWIND_INPUT}),
            'is_paid': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
            'salary_amount': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
            'duration_months': forms.NumberInput(attrs={'min': 1, 'class': TAILWIND_INPUT}),
            'location': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'deadline': forms.DateInput(
                attrs={'type': 'date', 'class': TAILWIND_INPUT},
                format='%Y-%m-%d',
            ),
            'is_active': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
        }

    def __init__(self, *args, is_edit=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not is_edit:
            # Новая стажировка всегда активна; управление видимостью — только в edit
            self.fields.pop('is_active')

    def save(self, company, commit=True):
        internship = super().save(commit=False)
        internship.company = company
        if not internship.slug:
            internship.slug = self._unique_slug(internship.title)
        if commit:
            internship.save()
        return internship

    @staticmethod
    def _unique_slug(title):
        base = slugify(title)[:240] or 'internship'
        slug, counter = base, 2
        while Internship.objects.filter(slug=slug).exists():
            slug = f'{base}-{counter}'
            counter += 1
        return slug
