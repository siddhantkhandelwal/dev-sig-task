from django import forms
from django.core import validators
import re


class Sign_up(forms.Form):
    team_name = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=20)
    id1 = forms.CharField(max_length=13, validators=[
        validators.RegexValidator(re.compile('^201[5-8]{1}[0-9A-Z]{4}[0-9]{4}P$'),
                                  message='Enter your valid BITS ID, for eg. 2018A7PS0210P')])
    id2 = forms.CharField(max_length=13, required=False, validators=[
        validators.RegexValidator(re.compile('^201[5-8]{1}[0-9A-Z]{4}[0-9]{4}P$'),
                                  message='Enter your valid BITS ID, for eg. 2018A7PS0210P')])


class LoginForm(forms.Form):
    team_name = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=20)
