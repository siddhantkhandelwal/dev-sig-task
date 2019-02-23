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
from django.core.exceptions import ValidationError
from datetime import datetime

current_question_key = 0
negative_marking_factor = 5

def index(request):
    if not request.user.is_authenticated:
        #The url endpoint below needs to be updated after the game is made.
        return redirect('/instructions')
    return redirect('/game')

def get_question_list(request):
    current_team = Team.objects.get(user = request.user)
    dushyant = current_team.questions_answered.all()
    dushyant_list = []
    for x in dushyant:
        dushyant_list.append(x.id)
    data = {'correct_list':dushyant_list}
    return JsonResponse(data)
    
def sign_up(request):
    if not request.user.is_authenticated: # This is to check that when user is logged in, he is not able to create a new team
        if request.method == 'POST':
            team_name = request.POST.get('teamname')
            # Next 2 lines are for Checking if the team_name has already been taken. This can be improved by using AJAX request (Frontend part)
            if User.objects.filter(username=team_name).exists():
                messages.error(request, "Sorry the Team Name has already been taken. Please try with some other team name")
                return render(request, 'Base/sign_up.html')
            password = request.POST.get('password')
            id1 = request.POST.get('id1')
            id2 = request.POST.get('id2')
            #------------------------------- ID VALIDATION STARTS-------------------------------------------------------
            val = [validators.RegexValidator(re.compile('^201[7-8]{1}[0-9A-Za-z]{4}[0-9]{4}[pP]$')),
                   validators.RegexValidator(re.compile('^201[4-6]{1}[0-9A-Za-z]{4}[0-9]{3}[pP]$')),]
            id1_flag = 1
            for validator in val :
                try :
                    error1 = validator(id1)
                    id1_flag = 0
                except ValidationError:
                    pass
            if id2 :
                id2_flag = 1 
                for validator in val :
                    try :
                        error2 = validator(id2)
                        id2_flag = 0
                    except ValidationError:
                        pass
            else :
                id2_flag = 0
            if id1_flag and id2_flag :
                messages.error(
                    request, 'ID - 1 and ID - 2 are both invalid')
                return render(request, 'Base/sign_up.html')
            elif id1_flag :
                messages.error(
                    request, 'ID - 1 is invalid')
                return render(request, 'Base/sign_up.html')
            elif id2_flag :
                messages.error(
                    request, 'ID - 2 is invalid')
                return render(request, 'Base/sign_up.html')
            #--------------------------------- ID VALIDATION ENDS----------------------------------------------------------
            ip = get_client_ip(request)
            user = User.objects.create_user(username=team_name, password=password)
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
            current_team = Team.objects.get(user=user)
            current_team.logged_in = 1
            current_team.save()
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
            current_team = Team.objects.get(user=user)
            if user and not current_team.logged_in:
                login(request, user)
                current_team.logged_in = 1
                current_team.save()
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
            # This is required to prevent the score from decreasing the score if someone has answered it correctly earlier
            if question in current_team.questions_answered.all():
                pass
            else :
                current_team.score = current_score - question.score_increment//negative_marking_factor
                current_team.save()
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
        if password=="#" or password=="admin" : # Todo : replace # by a custom administrator password of choice 
            current_user = Team.objects.get(user=request.user)
            current_user.logged_in = 0
            current_user.save()
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
    leaderboard = Team.objects.order_by('-score')
    A = []
    for a in leaderboard :
        A.append(a.user.username)
    current_user_rank = A.index(request.user.username)+1
    leaderboard = leaderboard[:9]
    Leaderboard = enumerate([[team.user.username, team.score]
                             for team in leaderboard], 1)
    return render(request, 'Base/leaderboard.html', {'Leaderboard': Leaderboard, 'rank': current_user_rank})


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

def instructions(request):
    return render(request, 'Base/instructions.html')

def time(request):
    try :
        FMT = "%H:%M:%S"
        timeout = datetime(year=2019, month=2, day=23, hour=22, minute=00, second=0, microsecond=0)
        time_now = datetime.now()
        # time_now = str(time_now.hour) + ":" + str(time_now.minute) + ":" + str(time_now.second)
        # time = datetime.strptime(timeout, FMT) - datetime.strptime(time_now, FMT)
        timediff = timeout - time_now
        timediff = str(timediff)
        # print(timediff)
        timeleft = int("0" + timediff[0])*60 + int(timediff[2:4])
        time = {
            'time': timeleft
        }
        return JsonResponse(time)
    except Exception:
        return JsonResponse({
            'time' : 0
        })