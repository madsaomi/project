import pytest
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.test import RequestFactory, TestCase
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.views import View

from apps.accounts.decorators import employer_required, student_required
from apps.accounts.mixins import EmployerRequiredMixin, StudentRequiredMixin

User = get_user_model()


@student_required
def dummy_student_view(request):
    return HttpResponse("Student OK")


@employer_required
def dummy_employer_view(request):
    return HttpResponse("Employer OK")


class DummyStudentCBV(StudentRequiredMixin, View):
    def get(self, request):
        return HttpResponse("Student CBV OK")


class DummyEmployerCBV(EmployerRequiredMixin, View):
    def get(self, request):
        return HttpResponse("Employer CBV OK")


class AccountsSecurityTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.student_user = User.objects.create_user(
            username='student1',
            email='student@example.com',
            password='password123',
            role=User.Role.STUDENT
        )
        self.employer_user = User.objects.create_user(
            username='employer1',
            email='employer@example.com',
            password='password123',
            role=User.Role.EMPLOYER
        )

    def test_student_required_decorator(self):
        request = self.factory.get('/dummy/')
        request.user = self.student_user
        response = dummy_student_view(request)
        self.assertEqual(response.status_code, 200)

        request.user = self.employer_user
        with self.assertRaises(Http404):
            dummy_student_view(request)

    def test_employer_required_decorator(self):
        request = self.factory.get('/dummy/')
        request.user = self.employer_user
        response = dummy_employer_view(request)
        self.assertEqual(response.status_code, 200)

        request.user = self.student_user
        with self.assertRaises(Http404):
            dummy_employer_view(request)

    def test_student_required_mixin(self):
        request = self.factory.get('/dummy/')
        request.user = self.student_user
        view = DummyStudentCBV.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request.user = self.employer_user
        with self.assertRaises(Http404):
            view(request)

    def test_employer_required_mixin(self):
        request = self.factory.get('/dummy/')
        request.user = self.employer_user
        view = DummyEmployerCBV.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request.user = self.student_user
        with self.assertRaises(Http404):
            view(request)


class AuthFlowTestCase(TestCase):
    def test_register_student(self):
        response = self.client.post('/accounts/register/', {
            'email': 'new@student.com',
            'password': 'testpass123',
            'role': 'student',
        })
        self.assertRedirects(response, '/internships/', fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(email='new@student.com').exists())

    def test_register_duplicate_email(self):
        User.objects.create_user(
            email='dup@test.com', username='dup', password='testpass123',
            role=User.Role.STUDENT,
        )
        response = self.client.post('/accounts/register/', {
            'email': 'dup@test.com', 'password': 'testpass123', 'role': 'student',
        })
        self.assertEqual(response.status_code, 400)

    def test_register_short_password(self):
        response = self.client.post('/accounts/register/', {
            'email': 'short@test.com', 'password': '123', 'role': 'student',
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email='short@test.com').exists())

    def test_login_valid_and_logout(self):
        User.objects.create_user(
            email='login@test.com', username='lg', password='testpass123',
            role=User.Role.EMPLOYER,
        )
        response = self.client.post('/accounts/login/', {
            'email': 'login@test.com', 'password': 'testpass123',
        })
        self.assertRedirects(response, '/internships/dashboard/', fetch_redirect_response=False)

        logout = self.client.post('/accounts/logout/')
        self.assertEqual(logout.status_code, 302)

    def test_login_invalid_credentials(self):
        response = self.client.post('/accounts/login/', {
            'email': 'ghost@test.com', 'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 400)

    def test_logout_requires_post(self):
        user = User.objects.create_user(
            email='po@test.com', username='po', password='testpass123',
            role=User.Role.STUDENT,
        )
        self.client.force_login(user)
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 405)


class PasswordResetTestCase(TestCase):
    def test_reset_flow_with_new_password(self):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes, force_str
        from django.utils.http import urlsafe_base64_encode

        user = User.objects.create_user(
            email='reset@test.com', username='rst', password='oldpassword1',
            role=User.Role.STUDENT,
        )

        # 1. Запрос сброса → письмо ушло, юзер-енумерации нет
        response = self.client.post('/accounts/password-reset/', {
            'email': 'reset@test.com',
        })
        self.assertRedirects(response, '/accounts/password-reset/done/')

        response_unknown = self.client.post('/accounts/password-reset/', {
            'email': 'ghost@nowhere.com',
        })
        self.assertEqual(response_unknown.status_code, 302)

        # 2. Ссылка подтверждения открывается (редирект на set-password — норма Django 5)
        uid = force_str(urlsafe_base64_encode(force_bytes(user.pk)))
        token = default_token_generator.make_token(user)
        confirm_url = f'/accounts/password-reset/{uid}/{token}/'
        response = self.client.get(confirm_url, follow=True)
        self.assertEqual(response.status_code, 200)

        # 3. Новый пароль сохраняется, старый больше не работает
        set_password_url = response.request['PATH_INFO']
        response = self.client.post(set_password_url, {
            'new_password1': 'brandnewpass99',
            'new_password2': 'brandnewpass99',
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertFalse(user.check_password('oldpassword1'))
        self.assertTrue(user.check_password('brandnewpass99'))

    def test_invalid_token_shows_error_page(self):
        user = User.objects.create_user(
            email='badtok@test.com', username='bt', password='testpass123',
            role=User.Role.STUDENT,
        )
        uid = force_str(urlsafe_base64_encode(force_bytes(user.pk)))
        response = self.client.get(f'/accounts/password-reset/{uid}/broken-token/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'недействительна')


class I18nTestCase(TestCase):
    def test_language_switch_translates_navbar(self):
        # Русский по умолчанию
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Стажировки')

        # Переключение на английский через set_language
        response = self.client.post('/i18n/setlang/', {'language': 'en'})
        self.assertEqual(response.status_code, 302)
        cookie = response.cookies['django_language']
        response = self.client.get('/', HTTP_COOKIE=f'django_language={cookie.value}')
        self.assertContains(response, 'Internships')
        self.assertNotContains(response, 'Зарегистрироваться')

    def test_uzbek_translation_applied(self):
        response = self.client.post('/i18n/setlang/', {'language': 'uz'})
        cookie = response.cookies['django_language'].value
        response = self.client.get('/', HTTP_COOKIE=f'django_language={cookie}')
        self.assertContains(response, 'Stajirovkalar')



class EdgeCasesTestCase(TestCase):
    """Ветки: banned-логин, ?next=, защита роли admin при регистрации."""

    @pytest.mark.django_db
    def test_banned_user_cannot_login(self):
        User.objects.create_user(
            email='banned@test.com', username='bn', password='testpass123',
            role=User.Role.STUDENT, is_banned=True,
        )
        response = self.client.post('/accounts/login/', {
            'email': 'banned@test.com', 'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 400)

    @pytest.mark.django_db
    def test_login_respects_next_param(self):
        User.objects.create_user(
            email='next@test.com', username='nx', password='testpass123',
            role=User.Role.STUDENT,
        )
        response = self.client.post(
            '/accounts/login/?next=/internships/my/',
            {'email': 'next@test.com', 'password': 'testpass123'},
        )
        self.assertRedirects(response, '/internships/my/', fetch_redirect_response=False)

    @pytest.mark.django_db
    def test_register_admin_role_forced_to_student(self):
        response = self.client.post('/accounts/register/', {
            'email': 'hacker@evil.com', 'password': 'testpass123', 'role': 'admin',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='hacker@evil.com')
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertFalse(user.is_staff)
