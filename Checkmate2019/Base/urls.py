from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("sign_out/", views.sign_out, name="sign_out"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("position/", views.position, name="position"),
    path("game/", views.game, name="game"),
    path("check_answer/", views.check_answer, name="check_answer"),
    path("display_score/", views.display_score, name="display_score"),
    path("get_question_list", views.get_question_list, name="get_question_list"),
    path("instructions/", views.instructions, name="instructions"),
    path("time/", views.time, name="time")
]
