from django import forms
from .models import Course
from django.forms import ModelForm, TextInput


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'e_mail', 'phone']
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control col-sm-8',
                    'placeholder': 'Фамилия и Имя',
                }),
            'phone': TextInput(
                attrs={
                    'class': 'form-control col-sm-8',
                    'placeholder': 'Телефон'
                }),
            'e_mail': TextInput(
                attrs={
                    'class': 'form-control col-sm-8',
                    'placeholder': 'Электронная почта'
                }),
        }


class HomeworkForm(forms.Form):
    homework = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}))
