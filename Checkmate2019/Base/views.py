from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Member
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import Sign_up, LoginForm
from django.http import HttpResponse
from django.contrib import messages
from ipware import get_client_ip
from django.contrib.auth.models import User


def index(request):
    if not request.user.is_authenticated:
        #The url endpoint below needs to be updated after the game is made.
        return render(request, "Base/index.html", {})
    return render(request, "Base/index.html", {})

    
def sign_up(request):
    if request.method == 'POST':
        form = Sign_up(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data.get('team_name')
            # Next 2 lines are for Checking if the team_name has already been taken. This can be improved by using AJAX request (Frontend part)
            if User.objects.filter(username=team_name).exists():
                return HttpResponse("Sorry the Team Name has already been taken. Please try with some other team name")
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(
                username=team_name, password=password)
            user.save()
            id1 = form.cleaned_data.get('id1')
            id2 = form.cleaned_data.get('id2')
            ip = get_client_ip(request)
            team = Team(user=user,
                        ip_address=ip, score=0, puzzles_solved=0, rank=0)
            team.save()
            member1 = Member(id=id1, team=team)
            member1.save()
            if id2:
                member2 = Member(id=id2, team=team)
                member2.save()
            messages.success(request, 'Team Successfully created!!')
            return redirect('/sign_in')
        else:
            form = Sign_up()
            messages.error(request, 'Please enter valid BITS IDs')
            return render(request, 'Base/sign_up.html', {'form': form})
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
                username=team_name, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Successfully logged in .')
                # Base/index written below needs to be updated after the game is completed.
                return render(request, 'Base/index.html')
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


@login_required
def leaderboard(request):
    leaderboard = Team.objects.order_by('rank')[:9]
    Leaderboard = enumerate([[team.user.username, team.score]
                             for team in leaderboard], 1)
    return render(request, 'Base/leaderboard.html', {'Leaderboard': Leaderboard})
