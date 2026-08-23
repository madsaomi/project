from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404, redirect, render

from .models import Conversation, Message


def _annotate_last_message(queryset):
    last_msg = Message.objects.filter(
        conversation=OuterRef('pk')
    ).order_by('-created_at')
    return queryset.annotate(
        last_message_content=Subquery(last_msg.values('content')[:1]),
        last_message_at=Subquery(last_msg.values('created_at')[:1]),
        last_message_sender_id=Subquery(last_msg.values('sender_id')[:1]),
    )


@login_required
def chat_list(request):
    """Список чатов пользователя (без N+1 на последнее сообщение)."""
    if request.user.role == 'student':
        conversations = _annotate_last_message(
            request.user.student_conversations.select_related('company')
        )
    elif request.user.role == 'employer':
        if not hasattr(request.user, 'company'):
            conversations = Conversation.objects.none()
        else:
            conversations = _annotate_last_message(
                request.user.company.conversations.select_related(
                    'student', 'student__student_profile'
                )
            )
    else:
        conversations = Conversation.objects.none()

    return render(request, 'messaging/list.html', {'conversations': conversations})

@login_required
def chat_detail(request, pk):
    if request.user.role == 'student':
        conversation = get_object_or_404(Conversation, pk=pk, student=request.user)
        other_party = conversation.company.name
    elif request.user.role == 'employer':
        conversation = get_object_or_404(Conversation, pk=pk, company=request.user.company)
        other_party = conversation.student.email
    else:
        return redirect('core:home')

    messages = conversation.messages.all().order_by('created_at')

    # Mark as read
    messages.exclude(sender=request.user).update(is_read=True)

    if request.headers.get('HX-Request'):
        return render(request, 'messaging/_message_feed.html', {
            'messages': messages,
            'conversation': conversation,
        })

    return render(request, 'messaging/chat.html', {
        'conversation': conversation,
        'messages': messages,
        'other_party': other_party
    })

@login_required
def send_message(request, pk):
    if request.method != 'POST':
        return redirect('messaging:detail', pk=pk)

    content = request.POST.get('content', '').strip()
    if not content:
        return redirect('messaging:detail', pk=pk)

    if request.user.role == 'student':
        conversation = get_object_or_404(Conversation, pk=pk, student=request.user)
    elif request.user.role == 'employer':
        conversation = get_object_or_404(Conversation, pk=pk, company=request.user.company)
    else:
        return redirect('core:home')

    Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=content
    )

    # Return updated message feed for HTMX
    messages = conversation.messages.all().order_by('created_at')
    return render(request, 'messaging/_message_feed.html', {
        'messages': messages,
        'conversation': conversation,
    })
