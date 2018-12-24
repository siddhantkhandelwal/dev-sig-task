from django.shortcuts import render, get_object_or_404, redirect
from .models import Team
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
            password = form.cleaned_data.get('password')
            id1 = form.cleaned_data.get('id1')
            id2 = form.cleaned_data.get('id2')
            ip = get_client_ip(request)
            team = Team(team_name=team_name, password=password,
                        ip_address=ip, score=0, puzzles_solved=0, rank=0, id1=id1, id2=id2)
            team.save()
            # Something wrong here as message is not being flashed
            messages.success(request, 'Team Successfully created!!')
            # on user side, but on admin site
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
