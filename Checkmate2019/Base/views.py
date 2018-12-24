from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Member
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import Sign_up, LoginForm
from django.http import HttpResponse
from django.contrib import messages
from ipware import get_client_ip
# from django.core.mail import send_mail can be used if we want to send mail to the players. we just need to create the emailaddress from
# id and the documentation for this can be found at https://docs.djangoproject.com/en/2.1/topics/forms/ under the section : Field Data


def index(request):
    if not request.user.is_authenticated:
        return render(request, "Base/index.html", {})
    return render(request, "Base/index.html", {})


def sign_up(request):
    if request.method == 'POST':
        form = Sign_up(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data.get('team_name')
            # Next 2 lines are for Checking if the team_name has already been taken. This can be improved by using AJAX request (Frontend part)
            if Team.objects.filter(team_name=team_name).exists():
                return HttpResponse("Sorry the Team Name has already been taken. Please try with some other team name")
            password = form.cleaned_data.get('password')
            id1 = form.cleaned_data.get('id1')
            id2 = form.cleaned_data.get('id2')
            ip = get_client_ip(request)
            team = Team(team_name=team_name, password=password,
                        ip_address=ip, score=0, puzzles_solved=0, rank=0)
            team.save()
            member1 = Member(id=id1, team=team)
            member1.save()
            if id2 :
                member2 = Member(id=id2, team=team)
                member2.save()
            # Something wrong here as message is not being flashed on user side, but on admin site
            messages.success(request, 'Team Successfully created!!')
            return redirect('/sign_in')
    else:
        form = Sign_up()
        return render(request, 'Base/sign_up.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data.get('team_name')
            password = form.cleaned_data.get('password')
            user = authenticate(
                request, team_name=team_name, password=password)
            if user:
                # Something wrong here as message is not being flashed
                messages.success(request, 'Successfully logged in .')
                # Base:game needs tom be updated after the game is completed.
                return redirect('Base:game')
            else:
                messages.error(
                    request, 'Login failed. Enter Correct Details .')  # Something wrong here as message is not being flashed
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


@login_required
def leaderboard(request):
    # Needs to be reviewed . It is not functioning properly
    Leaderboard = Team.objects.filter(rank <= 10)
    return render(request, 'Base/leaderboard.html', {'range': range(1, 11), 'Leaderboard': Leaderboard})
