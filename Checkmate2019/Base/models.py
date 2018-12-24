from django.db import models
from django.contrib.auth.models import User
from django.core import validators
import re


class Team(models.Model):
    team_name = models.CharField(max_length=25, primary_key=True)
    password = models.CharField(max_length=20)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    puzzles_solved = models.IntegerField(default=0)
    ip_address = models.CharField(null=True, max_length=20)
    id1 = models.CharField(default="2018A7PS0000P", max_length=13, validators=[
        validators.RegexValidator(re.compile('^201[5-8]{1}[0-9A-Z]{4}[0-9]{4}P$'),
                                  message='Enter your valid BITS ID, for eg. 2018A7PS0210P')])
    id2 = models.CharField(max_length=13, null=True, validators=[
        validators.RegexValidator(re.compile('^201[5-8]{1}[0-9A-Z]{4}[0-9]{4}P$'),
                                  message='Enter your valid BITS ID, for eg. 2018A7PS0210P')])

    def __str__(self):
        return f"{self.team_name} : {self.id1}   {self.id2}"
