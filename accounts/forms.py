from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
import re


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('already_registered')
        return email


class UserLoginResetForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']


class UserEmailResetForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']
