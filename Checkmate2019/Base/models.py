from django.db import models
from django.contrib.auth.models import User
from django.core import validators
import re


class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logged_in = models.BooleanField(default=0)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    puzzles_solved = models.IntegerField(default=0)
    ip_address = models.CharField(null=True, max_length=20)
    x_coordinates = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    y_coordinates = models.DecimalField(max_digits=10, decimal_places=5, default=0)

    def __str__(self):
        return self.user.username


class Member(models.Model):
    id = models.CharField(max_length=13, primary_key=True)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, blank=False, related_name="Member")

    def __str__(self):
        return self.id

class Question(models.Model):
    id = models.CharField(max_length=1000, primary_key=True)
    question_text = models.TextField(default="Test Question")
    answer = models.TextField(default="Test Answer")
    score_increment = models.IntegerField(default=10)
    answered_by = models.ManyToManyField(Team, related_name='questions_answered', blank=True)

    def __str__(self):
        return self.question_text
