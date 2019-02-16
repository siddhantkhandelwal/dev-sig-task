from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Member, Question
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from .forms import Sign_up, LoginForm
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from ipware import get_client_ip
from django.contrib.auth.models import User
import re
from django.core import validators

current_question_key = 0

def index(request):
    if not request.user.is_authenticated:
        #The url endpoint below needs to be updated after the game is made.
        return render(request, "Base/index.html", {})
    return render(request, "Base/index.html", {})

    
def sign_up(request):
    if not request.user.is_authenticated: # This is to check that when user is logged in, he is not able to create a new team
        if request.method == 'POST':
            team_name = request.POST.get('teamname')
            # Next 2 lines are for Checking if the team_name has already been taken. This can be improved by using AJAX request (Frontend part)
            if User.objects.filter(username=team_name).exists():
                messages.error(request, "Sorry the Team Name has already been taken. Please try with some other team name")
                return render(request, 'Base/sign_up.html')
            password = request.POST.get('password')
            user = User.objects.create_user(
                username=team_name, password=password)
            id1 = request.POST.get('id1')
            id2 = request.POST.get('id2')
            val = validators.RegexValidator(re.compile('^201[5-8]{1}[0-9A-Z]{4}[0-9]{4}P$'),
                                            message='Enter your valid BITS ID, for eg. 2018A7PS0210P')
            error = 0
            try:
                error1 = val(id1)
                if id2 :
                    error2 = val(id2)
            except Exception :
                error = 1
            if error:
                messages.error(
                    request, 'Enter your valid BITS ID')
                return render(request, 'Base/sign_up.html')
            ip = get_client_ip(request)
            user.save()
            team = Team(user=user,
                        ip_address=ip, score=0, puzzles_solved=0, rank=0)
            team.save()
            member1 = Member(id=id1, team=team)
            check_existence(request, id1) #If this bits id is registered with a team that has only one person, that team will be deleted. Otherwise nothing happens.
            member1.save()
            if id2:
                member2 = Member(id=id2, team=team)
                check_existence(request, id2)
                member2.save()
            # messages.success(request, 'Team Successfully created!!')
            user = authenticate(
                username=team_name, password=password)
            login(request, user)
            return redirect('/game')
        else:
            form = Sign_up()
            return render(request, 'Base/sign_up.html')   
    else :
        return redirect('/game')


def sign_in(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            team_name = request.POST.get('teamname')
            password = request.POST.get('password')
            user = authenticate(
                username=team_name, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Successfully logged in .')
                # Base/index written below needs to be updated after the game is completed.
                return redirect('/game')
            else:
                messages.error(
                    request, 'Login failed. Enter Correct Details .')
                return redirect('/sign_in')

        else:
            return render(request, 'Base/sign_in.html')
    else :
        return redirect('/game')

@login_required(login_url='/sign_in/')
@csrf_exempt
def game(request):
    if request.method == "POST":
        key = request.POST.get('questionKey')
        global current_question_key
        current_question_key = key
        question = Question.objects.get(id = key)
        question_text = question.question_text
        data = {
            'question_text':question_text
        }
        return JsonResponse(data)
    else:
        current_user = request.user
        current_team = Team.objects.get(user = current_user)
        score = current_team.score
        name = current_user.username
        return render(request, 'Base/main.html', {'teamname':name, 'score':score})


def check_answer(request):
    current_user = request.user
    current_team = Team.objects.get(user = current_user)
    current_score = current_team.score

    if request.method == "POST":
        answer = request.POST.get('answer')
        question = Question.objects.get(id = current_question_key)
        if answer == question.answer:
            if question in current_team.questions_answered.all(): #This is required to prevent the score from increasing if the somebody submits a correct answer to the same question more than once
                pass
            else:
                current_team.score = current_score + question.score_increment
                current_team.questions_answered.add(question)
                current_team.save()        
        else:
            pass
        return HttpResponse(status=204) #This means that the server has successfully processed the request and is not going to return any data.
    else:
        return HttpResponse("You weren't supposed to be here you know")

def display_score(request):
    current_user = request.user
    current_team = Team.objects.get(user = current_user)
    score = current_team.score
    if request.method == "POST":
        data = {
            'score':score
        }
        return JsonResponse(data)
    else:
        data = {
            'score':score
        }
        return JsonResponse(data)

@login_required
def sign_out(request):
    # we need to add a function here that will invoke the function : position and will store the coordinates
    if request.method=='POST':
        password = request.POST.get('password')
        if password=="#" : # Todo : replace # by a custom administrator password of choice 
            logout(request)
            messages.success(request, "You have been successfully logged out. We hope that you had a great time solving the puzzles. ")
            return redirect('/game')
        else :
            messages.error(request, 'Wrong password. contact invigilator.') 
            return redirect('/sign_out/')  
    else:
        return render(request, "Base/sign_out.html")

@login_required
def leaderboard(request):
    leaderboard = Team.objects.order_by('rank')[:9]
    Leaderboard = enumerate([[team.user.username, team.score]
                             for team in leaderboard], 1)
    return render(request, 'Base/leaderboard.html', {'Leaderboard': Leaderboard})


#Checks if a member is in a particular team. If the member is already in a team that has just one member, the team is deleted. Otherwise nothing happens to the team.
def check_existence(request, bitsid):
    if Member.objects.filter(id=str(bitsid)).exists():
        current_member = Member.objects.filter(id = str(bitsid))[0]
        current_team = current_member.team
        list_of_members = current_team.Member.all()
        if len(list_of_members) == 2:
            pass
        else:
            current_team.delete()
    else:
        pass

@login_required
def score(request):
    if request.method=="POST":
        score = request.POST['score']
        user = Team.objects.get(user=request.user)
        user.score += int(score)
        user.save()
        return redirect("/score") # needs to be updated after frontend is done
    else:
        #remove this part later....Currently its here only for a visual interface
        return render(request, 'Base/score.html', {})

#in case the user logs out of the system or the system crashes this functions comes into picture
@login_required
def position(request):
    if request.method=="POST":
        # Needs to be updated after frontend is done. input is to be taken not as a form, but every time the system crashes ot user logs out
        x_coordinates = request.POST['x_coordinates']
        y_coordinates = request.POST['y_coordinates']
        user = Team.objects.get(user=request.user)
        user.x_coordinates = float(x_coordinates)
        user.y_coordinates = float(y_coordinates)
        user.save()
        return redirect("/position")
    else :
        return render(request, 'Base/position.html', {})
