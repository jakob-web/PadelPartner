from bottle import route, run, template, static_file, request, redirect
from os import listdir
import user_registration
import user_login
import psycopg2
import profile

con = psycopg2.connect( 
    dbname="padelpartner", 
    user="ak1838",
    password="xrqhw4q4",
    host="pgserver.mah.se")

cur = con.cursor()

@route('/')
def index():
    cur.execute('select name from person')
    namn = cur.fetchall()
    return template('index.html', namn=namn)

@route('/logIn')
def logIn():
    return template('log_in.html', username ="")

@route('/register')
def register_form():
    """
    Shows a form for registration of a user.
    """
    return template("user_registration.html")

@route('/registerUser', method="POST")
def test():
    if user_registration.register() == True:
        return template("log_in.html",username="")

    elif user_registration.register() == False:
        print("Username already exists")
        return template("user_registration.html")

username = ''
img = ''
@route('/logInUser', method="POST")
def test2():
    if user_login.login() == True:
        global username
        username = getattr(request.forms, "userName")
        cur.execute("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
        global img
        img = cur.fetchone()
        # img = profile.getImg(username)
        # pid = "Select pid from registration where username = %s", [username]
        return template("welcome.html", picture = img, user = username)
        
    elif user_login.login() == False:
        return template("log_in.html", username = "")


@route('/changeProfile')
def changeProfile():
    
    return template("edit_profile.html",user = username)

@route('/profile', method="POST" )
def profil():
    
    profile.editProfile()
    return template("welcome.html", picture = img, user = username)


@route('/searchPlayers/')
def search():

    return template("search_players.html")
# TODO: Fix username auto fil lin when register form returns True


run(host='localhost', port=8080, debug=True)
con.close()