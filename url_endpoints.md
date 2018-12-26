This file consists of the list of URLS in the project
------------------------------------------------------------

<b>1. URL (Base/urls.py)   :</b> "/"
<b>   VIEW (Base/views.py) :</b> index
This is the home page . This url will return 2 different pages depending on whether the user is logged in or not. 
<br>
<b>2. URL (Base/urls.py)   :</b> "/sign_up/"
<b>   VIEW (Base/views.py) :</b> sign_up
This is the registration page for the team. 
<br>
<b>3. URL (Base/urls.py)   :</b> "/sign_in/"
<b>   VIEW (Base/views.py) :</b> sign_in
The team will enter their credentials on this page and shall be able to login.
<br>
<b>4. URL (Base/urls.py)   :</b> "/sign_out/"
<b>   VIEW (Base/views.py) :</b> sign_out
The user shall be logged out on making a get request to this url. 
<br>
<b>5. URL (Base/urls.py)   :</b> "/leaderboard/"
<b>   VIEW (Base/views.py) :</b> leaderboard
The team will be able to see the top 10 players on visiting this url. 