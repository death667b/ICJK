from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re
from .AuthResult import AUTH_RESULT
from django.core.exceptions import ValidationError

# Based off https://overiq.com/django/1.10/django-creating-users-using-usercreationform/
class StaffAccountCreationForm(forms.Form):
    email = forms.EmailField(label="Staff Email", required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    previous_error = AUTH_RESULT.NO_ERROR
    
    def clean_email(self):
        user_email = self.cleaned_data.get('email').lower()
        r = User.objects.filter(email=user_email)
        if r.count() > 0:
            self.previous_error = AUTH_RESULT.SIGNUP_EMAIL_IN_USE
            raise forms.ValidationError(
                "Email account exists"
            )

        m = re.findall('[\w\.\-_]+?\w+@icjk.com.au',user_email)
        if len(m) == 0:
            self.previous_error = AUTH_RESULT.SIGNUP_INVALID_EMAIL
            raise forms.ValidationError(
                "Email validation error"
            )

        return user_email
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password == None or password_confirm == None or password == '':
            self.previous_error = AUTH_RESULT.SIGNUP_INVALID_PASSWORD
            raise ValidationError(
                "Invalid password or confirmation"
            )

        if len(password) < 8:
            self.previous_error = AUTH_RESULT.SIGNUP_INVALID_PASSWORD
            raise ValidationError(
                "Password is less than 8 characters"
            )

        m = re.findall('([a-zA-Z])+', password)
        if len(m) == 0:
            self.previous_error = AUTH_RESULT.SIGNUP_INVALID_PASSWORD
            raise ValidationError(
                "Password is entirely numeric characters"
            )
        
        m = re.findall('([0-9])+', password)
        if len(m) == 0:
            self.previous_error = AUTH_RESULT.SIGNUP_INVALID_PASSWORD
            raise ValidationError(
                "Password is entirely alphabet characters"
            )
        
        if password != password_confirm:
            self.previous_error = AUTH_RESULT.SIGNUP_INVALID_CONFIRMATION
            raise ValidationError(
                "Passwords do not match"
            )


        return password_confirm

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        user_email = cleaned_data.get('email')
        
        if password and user_email:
            password = password.lower()
            user_email = user_email.lower()
            email_prefix = re.findall('([\w\.\-_]+?\w+)@icjk.com.au', user_email)
            if len(email_prefix) > 0 and password == email_prefix[0]:
                self.previous_error = AUTH_RESULT.SIGNUP_INVALID_PASSWORD
                raise ValidationError(
                    "Password is too similar to email address"
                )


    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )
        return user