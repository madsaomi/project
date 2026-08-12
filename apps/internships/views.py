import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import employer_required, student_required
from .models import Internship, InternshipParticipant

def catalog(request):
    qs = Internship.objects.filter(is_active=True).select_related('company', 'category')
    
    if work_format := request.GET.get('work_format'):
        qs = qs.filter(work_format=work_format)
    if is_paid := request.GET.get('is_paid'):
        qs = qs.filter(is_paid=is_paid == 'true')
        
    if request.headers.get('HX-Request'):
        return render(request, 'internships/_list.html', {'internships': qs})
    return render(request, 'internships/catalog.html', {'internships': qs})

def detail(request, slug):
    internship = get_object_or_404(Internship, slug=slug, is_active=True)
    
    applied = False
    if request.user.is_authenticated and request.user.role == 'student':
        applied = InternshipParticipant.objects.filter(internship=internship, student=request.user).exists()
        
    return render(request, 'internships/detail.html', {
        'internship': internship,
        'applied': applied
    })

@login_required
@student_required
def apply(request, slug):
    internship = get_object_or_404(Internship, slug=slug, is_active=True)
    participant, created = InternshipParticipant.objects.get_or_create(
        internship=internship, student=request.user
    )
    
    response = render(request, 'internships/_apply_btn.html', {'applied': True})
    response['HX-Trigger'] = json.dumps({'show-toast': {'message': 'Отклик отправлен!', 'type': 'success'}})
    return response

@login_required
@employer_required
def create(request):
    # TODO: Implement form processing
    return render(request, 'internships/create.html')

@login_required
@employer_required
def dashboard(request):
    # TODO: Implement kanban board logic
    company = request.user.company
    # Example logic: Get all participants for this company's internships
    participants = InternshipParticipant.objects.filter(internship__company=company).select_related('student', 'internship')
    
    return render(request, 'internships/dashboard.html', {
        'participants': participants
    })
