from bottle import route, run, template, static_file, request, redirect
from os import listdir
import user_registration
import user_login
import psycopg2
import profile
import show_match

con = psycopg2.connect( 
    dbname="filipspadel", 
    user="ak1838",
    password="xrqhw4q4",
    host="pgserver.mah.se")

cur = con.cursor()

username = ''
img = ''

@route('/')
def index():
    cur.execute('select name from person')
    namn = cur.fetchall()
    return template('index.html', namn=namn)

@route('/static/<filename>') 
def static_files(filename):  
    return static_file(filename, root="static")

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


@route('/logInUser', method="POST")
def test2():
    if user_login.login() == True:
        global username
        username = getattr(request.forms, "userName")
        cur.execute("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
        global img
        img = cur.fetchone()

        profileInfo = []
        cur.execute("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
        profileInfo = cur.fetchall()

        cur.execute("select name from(person join registration on person.pid = registration.pid) where username = %s", [username])
        personName = cur.fetchone()
        print(personName)
        print(username)
        # img = profile.getImg(username)
        # pid = "Select pid from registration where username = %s", [username]
        return template("welcome.html", picture = img, user = username, profileInfo = profileInfo, personName = personName)
        
    elif user_login.login() == False:
        return template("log_in.html", username = "")


@route('/changeProfile')
def changeProfile():
    
    return template("edit_profile.html",user = username)

@route('/profile', method="POST" )
def profil():
    global username
    profile.editProfile(username)
    cur.execute("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
    global img
    img = cur.fetchone()

    profileInfo = []
    cur.execute("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
    profileInfo = cur.fetchall()

    return template("welcome.html", picture = img, user = username, profileInfo = profileInfo)


@route('/createMatch')
def create():

    return template("create_match.html", username = username)



@route('/findMatch', method="POST")
def findMatch():
    global ort
    ort = getattr(request.forms, "ort")
    
    show_match.createGame(username)

    return template("find_match.html", games=show_match.findGame(ort))
    
       

@route('/show_games')
def showGame():
    return template("show_match.html")

@route('/show_match', method="POST")
def showMatch():
    
    ort = getattr(request.forms, "ort")
       
    return template("find_match.html", games=show_match.showGame(ort))

@route('/showMatchProfile/<matchid>')
def showMatchProfile(matchid):
    global username 
    
    matchid = matchid
    return template("match_profile.html", match = show_match.showMatchProfile(matchid))

# TODO: Fix username auto fil lin when register form returns True


run(host='localhost', port=8080, debug=True)
con.close()