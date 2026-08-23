from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import StudentProfile
from .services.docx_exporter import generate_resume_docx
from .services.pdf_exporter import generate_resume_pdf


def _get_visible_profile(request, pk):
    """Резюме видно всем, если is_public; приватное — только владельцу."""
    profile = get_object_or_404(StudentProfile, pk=pk)
    if not profile.is_public and request.user != profile.user:
        raise Http404
    return profile


@login_required
def builder(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name', '')
        profile.headline = request.POST.get('headline', '')
        profile.about = request.POST.get('about', '')
        profile.institution = request.POST.get('institution', '')
        profile.specialty = request.POST.get('specialty', '')
        profile.save()
        return redirect('profiles:viewer', pk=profile.pk)

    return render(request, 'profiles/builder.html', {'profile': profile})


def viewer(request, pk):
    profile = _get_visible_profile(request, pk)
    return render(request, 'profiles/viewer.html', {'profile': profile})

def export_pdf(request, pk):
    profile = _get_visible_profile(request, pk)
    pdf_content = generate_resume_pdf(profile, request)
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{profile.pk}.pdf"'
    return response

def export_docx(request, pk):
    profile = _get_visible_profile(request, pk)
    docx_content = generate_resume_docx(profile)
    docx_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    response = HttpResponse(docx_content, content_type=docx_type)
    response['Content-Disposition'] = f'attachment; filename="resume_{profile.pk}.docx"'
    return response
