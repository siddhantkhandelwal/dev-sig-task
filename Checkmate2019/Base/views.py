from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Member
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import TeamForm, MemberForm, LoginForm
from django.http import HttpResponse
from django.contrib import messages
from ipware import get_client_ip
# from django.core.mail import send_mail can be used if we want to send mail to the players. we just need to create the emailaddress from
# id and the documentation for this can be found at https://docs.djangoproject.com/en/2.1/topics/forms/ under the section : Field Data


def index(request):
    if not request.user.is_authenticated:
        return render(request, "Base/index.html", {})
    return render(request, "Base/index.html", {})


def sign_up_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data.get('team_name')
            password = form.cleaned_data.get('password')
            ip = get_client_ip(request)
            team = Team(team_name=team_name, password=password,
                        ip_address=ip, score=0, puzzles_solved=0, rank=0)
            team.save()
            # flash message
            messages.success(request, 'Team Successfully created!!')
            return redirect('/sign_up_Member')
    else:
        form = TeamForm()
        return render(request, 'Base/sign_up_team.html', {'form': form})


def sign_up_Member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('id')
            team_name = form.cleaned_data.get('team_name')
            team = Team.objects.get(team_name=team_name)
            member = Member(id=id, team=team)
            member.save()
            messages.success(request, 'User successfully added. ')
            # The design needs to be modified so  that after submitting the form 2 times the user is
            return redirect('/sign_up_Member')
            # redirected to the login page .
        else:
            return HttpResponse("There was some error, please try again. ")
    else:
        form = MemberForm()
        return render(request, 'Base/sign_up_Member.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data.get('team_name')
            password = form.cleaned_data.get('password')
            user = authenticate(
                request, team_name=team_name, password=password)
            if user:
                messages.success(request, 'Successfully logged in .')
                # Base:game needs tom be updated after the game is completed.
                return redirect('Base:game')
            else:
                messages.error(
                    request, 'Login failed. Enter Correct Details .')
                return redirect('/sign_in')
        else:
            return HttpResponse("There was some error, please try again.")
    else:
        form = LoginForm()
        return render(request, 'Base/sign_in.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    return HttpResponse("You have been successfully logged out. We hope that you had a great time solving the puzzles. ")


def leaderboard(request):
    # Needs to be reviewed . It is not functioning properly
    Leaderboard = Team.objects.filter(rank <= 10)
    return render(request, 'Base/leaderboard.html', {'range': range(1, 11), 'Leaderboard': Leaderboard})
