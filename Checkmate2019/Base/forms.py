from django import forms
from django.core import validators
import re

class TeamForm(forms.Form):
    team_name = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput() , max_length=20)

class MemberForm(forms.Form):
    id = forms.CharField(max_length=13, validators=[
        validators.RegexValidator(re.compile('^201[5-8]{1}[0-9A-Z]{4}[0-9]{4}P$'),
        message='Enter your valid BITS ID, for eg. 2018A7PS0210P')])
    team_name = forms.CharField(max_length=25)

class LoginForm(forms.Form):
    team_name = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=20)
    