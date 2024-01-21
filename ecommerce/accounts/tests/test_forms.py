# users/tests/test_forms.py

from django.test import TestCase
from accounts.forms import CustomUserCreationForm


class CustomUserCreationFormTest(TestCase):
    def test_form_has_fields(self):
        form = CustomUserCreationForm()
        expected_fields = ["username", "email", "password1", "password2"]
        actual_fields = list(form.fields)
        self.assertSequenceEqual(expected_fields, actual_fields)

    # Add more tests to validate your form behavior...
