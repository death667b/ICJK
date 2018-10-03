from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re
from .SignupResult import SIGNUP_RESULT
from django.core.exceptions import ValidationError

# Based off https://overiq.com/django/1.10/django-creating-users-using-usercreationform/
class StaffAccountCreationForm(forms.Form):
    email = forms.EmailField(label="Staff Email", required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    previous_error = SIGNUP_RESULT.NO_ERROR
    
    def clean_email(self):
        user_email = self.cleaned_data.get('email').lower()
        r = User.objects.filter(email=user_email)
        if r.count() is not 0:
            self.previous_error = SIGNUP_RESULT.EMAIL_IN_USE
            raise forms.ValidationError(
                "Email account exists"
            )

        m = re.findall('([\w\.\-_]+)?\w+@icjk.com.au',user_email)
        if m is None or len(m) is not 1:
            self.previous_error = SIGNUP_RESULT.INVALID_EMAIL
            raise forms.ValidationError(
                "Email validation error"
            )

        return user_email
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password == None or password_confirm == None or password == '':
            self.previous_error = SIGNUP_RESULT.INVALID_PASSWORD
            raise ValidationError(
                "Invalid password or confirmation"
            )

        if password != password_confirm:
            self.previous_error = SIGNUP_RESULT.INVALID_CONFIRMATION
            raise ValidationError(
                "Passwords do not match"
            )

        return password_confirm

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )
        return user