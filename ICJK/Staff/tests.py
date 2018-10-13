from django.test import TestCase
from .StaffAccountCreationForm import StaffAccountCreationForm
from django.test.client import RequestFactory
from django.http import Http404, HttpRequest
from django.forms import ValidationError
from .AuthResult import AUTH_RESULT
from django.contrib.auth.models import User
# Create your tests here.

class StaffAccountCreationFormTests(TestCase):

    def create_user(self, email, password):
        try:
            u = User.objects.get(email=email)
            self.delete_user(email)
        except User.DoesNotExist:
            pass
        form = StaffAccountCreationForm({
            'email':email,
            'password': password,
            'password_confirm': password
        })
        form.is_valid()
        return form.save()

    def delete_user(self, email):
        try:
            u = User.objects.get(email=email)
            u.delete()
        except User.DoesNotExist:
            pass

    def test_form_creation(self):
        form = None
        try:
            form = StaffAccountCreationForm({
                'email':'user@icjk.com.au',
                'password':'p45sword1235',
                'password_confirm':'p45sword1235'
            })
        except Exception:
            pass
        self.assertIsNotNone(form)

    def test_password_similarity(self):
        form = StaffAccountCreationForm({
                'email':'staffaccount12@icjk.com.au',
                'password':'staffaccount12',
                'password_confirm':'staffaccount12'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_PASSWORD)

    def test_small_password(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@icjk.com.au',
                'password':'smolpwd',
                'password_confirm':'smolpwd'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_PASSWORD)

    def test_numeric_only_password(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@icjk.com.au',
                'password':'4815162342',
                'password_confirm':'4815162342'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_PASSWORD)

    def test_alpha_only_password(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@icjk.com.au',
                'password':'staffpassword',
                'password_confirm':'staffpassword'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_PASSWORD)

    def test_non_staff_email(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@gmail.com',
                'password':'p45sword1235',
                'password_confirm':'p45sword1235'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_EMAIL)

    def test_existing_email(self):
        user_email = 'staff_test@icjk.com.au'
        user_password = 'p45sword1235'
        self.create_user(user_email, user_password)
        form = StaffAccountCreationForm({
                'email':user_email,
                'password':user_password,
                'password_confirm':user_password
            })
        res = form.is_valid()
        self.delete_user(user_email)
        self.assertEqual(res, False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_EMAIL_IN_USE)

    def test_invalid_email(self):
        form = StaffAccountCreationForm({
                'email':'not_an_email$icjk.com.au',
                'password':'p45sword1235',
                'password_confirm':'p45sword1235'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_EMAIL)

    def test_different_password_confirmation(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@gmail.com',
                'password':'p45sword1235',
                'password_confirm':'password54321'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_PASSWORD)

    def test_working_combination(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@icjk.com.au',
                'password':'p45sword1235',
                'password_confirm':'p45sword1235'
            })
        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.previous_error, AUTH_RESULT.NO_ERROR)


class StaffLoginFormTests(TestCase):
    def test_invalid_email(self):
        pass

    def test_unknown_email(self):
        pass

    def test_invalid_password(self):
        pass

    def test_working_combination(self):
        pass

