from django import forms
from .models import State, People
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class DateInput(forms.DateInput):
    input_type='date'


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ('date', 'people')
        labels = {
        	'people':_('Ученики'),
            'date':_('Дата')
        }
        widgets = {
            'date': DateInput(),
            }

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        max_length=100,
        error_messages={'required': 'Укажите логин'})
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        error_messages={'required': 'Укажите пароль'})
    widgets = {'password': forms.PasswordInput()}

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        max_length=100,
        error_messages={'required': 'Укажите логин'})
    email = forms.EmailField(
        label='Электронная почта')
    first_name = forms.CharField(
        label='Имя',
        max_length=100,
        error_messages={'required': 'Укажите имя'})
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        error_messages={'required': 'Укажите фамилию'})
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        error_messages={'required': 'Укажите пароль'})
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput,
        error_messages={'required': 'Укажите повтор пароля'})
    widgets = {'password1': forms.PasswordInput(), 'password2': forms.PasswordInput()}

class PasrecForm(forms.Form):
    password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput,
        error_messages={'required': 'Укажите старый пароль'})
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        error_messages={'required': 'Укажите новый пароль'})
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput,
        error_messages={'required': 'Укажите повтор нового пароля'})
    widgets = {'password1': forms.PasswordInput(), 'password2': forms.PasswordInput(), 'password': forms.PasswordInput()}