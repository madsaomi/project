from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Conversation, Message
from apps.companies.models import Company

@login_required
def chat_list(request):
    if request.user.role == 'student':
        conversations = request.user.student_conversations.all().select_related('company')
    elif request.user.role == 'employer':
        # Ensure company exists
        if not hasattr(request.user, 'company'):
            return render(request, 'messaging/list.html', {'conversations': []})
        conversations = request.user.company.conversations.all().select_related('student', 'student__student_profile')
    else:
        conversations = []
        
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
        return render(request, 'messaging/_message_feed.html', {'messages': messages, 'conversation': conversation})

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
    return render(request, 'messaging/_message_feed.html', {'messages': messages, 'conversation': conversation})
