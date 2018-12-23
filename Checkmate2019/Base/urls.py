from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sign_up_team/", views.sign_up_team , name="sign_up_team"),
    path("sign_up_Member/", views.sign_up_Member, name="sign_up_Member"), 
    path("sign_in/", views.sign_in, name="sign_in"),
    path("sign_out/", views.sign_out, name="sign_out"),
    path("leaderboard/", views.leaderboard, name="leaderboard")
]
