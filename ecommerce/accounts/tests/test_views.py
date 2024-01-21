# users/tests/test_views.py

from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import CustomUserCreationForm
from accounts.views import SignUpView, LoginView


class LoginViewTest(TestCase):
    def setUp(self):
        url = reverse("login")
        self.response = self.client.get(url)

    def test_login_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_login_url_resolves_login_view(self):
        view = resolve("/accounts/login/")
        self.assertEqual(view.func.view_class, LoginView)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, AuthenticationForm)

    # Add more tests for form validation, redirection, etc.


class SignUpViewTest(TestCase):
    def setUp(self):
        url = reverse("signup")
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve("/accounts/signup/")
        self.assertEqual(view.func.view_class, SignUpView)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, CustomUserCreationForm)

    # Add more tests for form validation, redirection, etc.
