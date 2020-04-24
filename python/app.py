from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
from os import listdir
import user_registration
import user_login
import psycopg2
import profile
import show_match
app = Flask(__name__)
con = psycopg2.connect( 
    dbname="tennispartner", 
    user="ak3672",
    password="294evcub",
    host="pgserver.mah.se")

cur = con.cursor()

username = ''
img = ''

@app.route('/')
def index():
    cur.execute('select name from person')
    namn = cur.fetchall()
    return render_template('index.html', namn=namn)

@app.route('/static/<filename>') 
def static_files(filename):  
    return static_file(filename, root="static")

@route('/logIn')
def logIn():
    return render_template('log_in.html', username ="")

@app.route('/register')
def register_form():
    """
    Shows a form for registration of a user.
    """
    return render_template("user_registration.html")

@app.route('/registerUser' , methods=['GET', 'POST'])
def test():
    if user_registration.register() == True:
        return render_template("log_in.html",username="")

    elif user_registration.register() == False:
        print("Username already exists")
        return render_template("user_registration.html")


@app.route('/logInUser', methods=['GET', 'POST'])
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
        return render_template("welcome.html", picture = img, user = username, profileInfo = profileInfo, personName = personName)
        
    elif user_login.login() == False:
        return render_template("log_in.html", username = "")


@app.route('/changeProfile')
def changeProfile():
    cur.execute("select * from (profile join registration on profile.pid = registration.pid) where username = %s", [username])
    informationProfile = cur.fetchall()
    print(informationProfile)
    return render_template("edit_profile.html",user = username, info = informationProfile)

@app.route('/profile', methods=['GET', 'POST'])
def profil():
    global username
    profile.editProfile(username)
    cur.execute("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
    global img
    img = cur.fetchone()

    profileInfo = []
    cur.execute("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
    profileInfo = cur.fetchall()
    cur.execute("select name from(person join registration on person.pid = registration.pid) where username = %s", [username])
    personName = cur.fetchone()

    return render_template("welcome.html", picture = img, user = username, profileInfo = profileInfo, personName = personName)


@app.route('/createMatch')
def create():

    return render_template("create_match.html", username = username)



@app.route('/findMatch', methods=['GET', 'POST'])
def findMatch():
    global ort
    ort = getattr(request.forms, "ort")
    
    show_match.createGame(username)

    return render_template("find_match.html", games=show_match.findGame(ort))
    
       

@app.route('/show_games')
def showGame():
    return render_template("show_match.html")

@app.route('/show_match', methods=['GET', 'POST'])
def showMatch():
    
    ort = getattr(request.forms, "ort")
    klass = getattr(request.forms, "klass")
    antal = getattr(request.forms, "antal")
       
    return render_template("find_match.html", games=show_match.showGame(ort,klass,antal))

@app.route('/showMatchProfile/<matchid>')
def showMatchProfile(matchid):
    global username 
    
    matchid = matchid
    return render_template("match_profile.html", match = show_match.showMatchProfile(matchid))

# TODO: Fix username auto fil lin when register form returns True

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8080, debug=True)


con.close()
