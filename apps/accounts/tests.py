from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404
from django.views import View

from apps.accounts.decorators import student_required, employer_required
from apps.accounts.mixins import StudentRequiredMixin, EmployerRequiredMixin

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
