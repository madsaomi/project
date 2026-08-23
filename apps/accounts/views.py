from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import redirect, render

from .models import User


def register_view(request):
    """Регистрация пользователя с выбором роли (student/employer)."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'student')
        if role not in User.Role.values or role == User.Role.ADMIN:
            role = User.Role.STUDENT

        error = None
        if not email or '@' not in email:
            error = 'Укажите корректный email.'
        elif len(password) < 8:
            error = 'Пароль должен быть не короче 8 символов.'
        elif User.objects.filter(email=email).exists():
            error = 'Пользователь с таким email уже существует.'

        if error:
            return render(
                request, 'accounts/register.html', {'error': error}, status=400
            )

        user = User.objects.create_user(
            email=email,
            username=email,
            role=role,
            password=password,
            accepted_terms=True,
        )
        login(request, user)

        # Работодателю сразу нужен профиль компании, студенту — каталог
        if role == User.Role.EMPLOYER:
            return redirect('companies:profile_edit')
        return redirect('internships:catalog')

    return render(request, 'accounts/register.html')


def login_view(request):
    """Вход по email и паролю."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)
        if user is None or not user.is_active or user.is_banned:
            return render(
                request,
                'accounts/login.html',
                {'error': 'Неверный email или пароль.'},
                status=400,
            )

        login(request, user)
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        if user.role == User.Role.EMPLOYER:
            return redirect('internships:dashboard')
        return redirect('internships:my_internships')

    return render(request, 'accounts/login.html')


class LogoutView(DjangoLogoutView):
    """Выход (только POST)."""
    next_page = '/'
