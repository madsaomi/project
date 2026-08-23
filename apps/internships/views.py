import json

from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count, OuterRef, Subquery
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.accounts.decorators import employer_required, student_required
from apps.messaging.models import Conversation

from .forms import InternshipForm
from .models import Internship, InternshipParticipant


def _with_conversation_id(queryset):
    """Аннотирует отклики id диалога со компанией (устраняет N+1 в шаблонах)."""
    return queryset.annotate(
        conversation_id=Subquery(
            Conversation.objects.filter(
                company=OuterRef('internship__company_id'),
                student=OuterRef('student_id'),
            ).values('pk')[:1]
        )
    )


def catalog(request):
    """Каталог активных стажировок с поиском и фильтрами (HTMX)."""
    qs = (
        Internship.objects
        .filter(is_active=True)
        .select_related('company', 'category')
    )

    if query := request.GET.get('q'):
        from django.db.models import Q

        qs = qs.filter(
            Q(title__icontains=query)
            | Q(company__name__icontains=query)
            | Q(description__icontains=query)
        )
    if category_slug := request.GET.get('category'):
        qs = qs.filter(category__slug=category_slug)
    if work_format := request.GET.get('work_format'):
        qs = qs.filter(work_format=work_format)
    if is_paid := request.GET.get('is_paid'):
        qs = qs.filter(is_paid=is_paid == 'true')

    context = {'internships': qs}
    if not request.headers.get('HX-Request'):
        from .models import Category

        context['categories'] = Category.objects.all()
    template = 'internships/_list.html' if request.headers.get('HX-Request') else \
        'internships/catalog.html'
    return render(request, template, context)


def detail(request, slug):
    """Страница стажировки."""
    internship = get_object_or_404(
        Internship.objects.select_related('company', 'category'),
        slug=slug,
        is_active=True,
    )
    Internship.objects.filter(pk=internship.pk).update(views_count=models.F('views_count') + 1)

    applied = False
    if request.user.is_authenticated and request.user.role == 'student':
        applied = InternshipParticipant.objects.filter(
            internship=internship, student=request.user
        ).exists()

    return render(request, 'internships/detail.html', {
        'internship': internship,
        'applied': applied
    })

@login_required
@student_required
def apply(request, slug):
    """Отклик студента на стажировку (HTMX). Создаёт диалог с компанией."""
    internship = get_object_or_404(Internship, slug=slug, is_active=True)

    already_applied = InternshipParticipant.objects.filter(
        internship=internship, student=request.user
    ).exists()

    if not already_applied:
        deadline_passed = internship.deadline and internship.deadline < timezone.now().date()
        if deadline_passed:
            response = render(request, 'internships/_apply_btn.html', {
                'applied': False,
                'internship': internship,
            })
            toast = {'message': 'Приём откликов по этой стажировке окончен', 'type': 'error'}
            response['HX-Trigger'] = json.dumps({'show-toast': toast})
            return response

        InternshipParticipant.objects.get_or_create(
            internship=internship, student=request.user
        )
        Conversation.objects.get_or_create(
            company=internship.company, student=request.user
        )
        response = render(request, 'internships/_apply_btn.html', {'applied': True})
        toast = {'message': 'Отклик отправлен!', 'type': 'success'}
        response['HX-Trigger'] = json.dumps({'show-toast': toast})
        return response

    return render(request, 'internships/_apply_btn.html', {'applied': True})

ALLOWED_TRANSITIONS = {
    'active': {'pending'},
    'completed': {'active'},
    'cancelled': {'pending', 'active'},
}

@login_required
@employer_required
@require_POST
def update_participant_status(request, pk):
    """Смена статуса отклика работодателем (Kanban, HTMX)."""
    participant = get_object_or_404(
        InternshipParticipant.objects.select_related('internship__company'),
        pk=pk,
    )

    # Http404 вместо 403 — не раскрываем существование чужого объекта
    if participant.internship.company.user != request.user:
        raise Http404

    new_status = request.POST.get('status')
    allowed_from = ALLOWED_TRANSITIONS.get(new_status, set())
    if not new_status or participant.status not in allowed_from:
        toast = {'message': 'Недопустимый переход статуса', 'type': 'error'}
        response = render(request, 'internships/_participant_card.html',
                          {'p': participant})
        response['HX-Trigger'] = json.dumps({'show-toast': toast})
        return response

    participant.status = new_status
    now = timezone.now()
    if new_status == 'active' and not participant.start_date:
        participant.start_date = now.date()
    elif new_status == 'completed':
        if not participant.start_date:
            participant.start_date = now.date()
        participant.end_date = now.date()
        participant.completed_at = now
    participant.save()

    response = render(request, 'internships/_participant_card.html', {'p': participant})
    toast = {'message': 'Статус обновлён', 'type': 'success'}
    response['HX-Trigger'] = json.dumps({'show-toast': toast})
    return response

@login_required
@student_required
def my_internships(request):
    """Дашборд студента: его отклики и статусы."""
    applications = _with_conversation_id(
        InternshipParticipant.objects
        .filter(student=request.user)
        .select_related('internship__company')
        .order_by('-created_at')
    )
    stats = {
        'total': applications.count(),
        'pending': applications.filter(status='pending').count(),
        'active': applications.filter(status='active').count(),
        'completed': applications.filter(status='completed').count(),
    }
    return render(request, 'internships/my_internships.html', {
        'applications': applications,
        'stats': stats,
    })

@login_required
@employer_required
def create(request):
    """Публикация новой стажировки."""
    if not hasattr(request.user, 'company'):
        return redirect('companies:profile_edit')

    form = InternshipForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        internship = form.save(request.user.company)
        return redirect('internships:detail', slug=internship.slug)

    return render(request, 'internships/form.html', {
        'form': form,
        'is_edit': False,
    })

@login_required
@employer_required
def edit(request, slug):
    """Редактирование своей стажировки (и закрытие набора через is_active)."""
    internship = get_object_or_404(
        Internship.objects.select_related('company'), slug=slug
    )

    # Http404 вместо 403 — не раскрываем существование чужого объекта
    if internship.company.user != request.user:
        raise Http404

    form = InternshipForm(request.POST or None, instance=internship, is_edit=True)
    if request.method == 'POST' and form.is_valid():
        form.save(internship.company)
        return redirect('internships:detail', slug=internship.slug)

    return render(request, 'internships/form.html', {
        'form': form,
        'is_edit': True,
        'internship': internship,
    })

@login_required
@employer_required
def dashboard(request):
    """Kanban-доска работодателя: отклики на стажировки его компании."""
    if not hasattr(request.user, 'company'):
        return render(request, 'internships/dashboard.html', {'participants': []})

    participants = _with_conversation_id(
        InternshipParticipant.objects
        .filter(internship__company=request.user.company)
        .select_related('student__student_profile', 'internship')
        .order_by('-created_at')
    )
    company_internships = (
        Internship.objects
        .filter(company=request.user.company)
        .annotate(applications_count=Count('participants'))
        .order_by('-created_at')
    )
    return render(request, 'internships/dashboard.html', {
        'participants': participants,
        'company_internships': company_internships,
        'pending_count': sum(1 for p in participants if p.status == 'pending'),
        'active_count': sum(1 for p in participants if p.status == 'active'),
        'completed_count': sum(
            1 for p in participants
            if p.status in ('completed', 'cancelled')
        ),
    })
