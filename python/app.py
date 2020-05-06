from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
from os import listdir
import user_registration
import user_login
import profile
import show_match
from db_operations import fetchone, fetchmany, fetchall

import psycopg2
app = Flask(__name__)
<<<<<<< Updated upstream
conn = psycopg2.connect( 
    dbname="padelpar", 
    user="aj7951",
    password="ez2g1c1h",
    host="pgserver.mah.se")

cur = conn.cursor()
=======
>>>>>>> Stashed changes

username = ''
img = ''

@app.route('/')
def index():
    return render_template('log_in.html', username = username)

@app.route('/logIn')
def logIn():
    return render_template('log_in.html', username = username)

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
        username = request.form["userName"]
        global img
<<<<<<< Updated upstream
        img = cur.fetchone()
        conn.commit()
        cur.close()

        profileInfo = []
        cur.execute("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
        profileInfo = cur.fetchall()
        conn.commit()
        cur.close()

        cur.execute("select name from(person join registration on person.pid = registration.pid) where username = %s", [username])
        personName = cur.fetchone()
        conn.commit()
        cur.close()
        print(personName)
        print(username)
=======
        img = fetchone("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
        profileInfo = []
        profileInfo = fetchall("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [username])

        personName = fetchone("select name from(person join registration on person.pid = registration.pid) where username = %s", [username])
>>>>>>> Stashed changes
        # img = profile.getImg(username)
        # pid = "Select pid from registration where username = %s", [username]
        return render_template("welcome.html", picture = img, user = username, profileInfo = profileInfo, personName = personName)

    elif user_login.login() == False:
        return render_template("log_in.html", username = "")


@app.route('/changeProfile')
def changeProfile():
<<<<<<< Updated upstream
    cur.execute("select * from (profile join registration on profile.pid = registration.pid) where username = %s", [username])
    informationProfile = cur.fetchall()
    conn.commit()
    cur.close()
=======
    informationProfile = fetchall("select * from (profile join registration on profile.pid = registration.pid) where username = %s", [username])
>>>>>>> Stashed changes
    print(informationProfile)
    return render_template("edit_profile.html",user = username, info = informationProfile)

@app.route('/profile', methods=['GET', 'POST'])
def profil():
    global username
    profile.editProfile(username)
    global img
<<<<<<< Updated upstream
    img = cur.fetchone()
    conn.commit()
    cur.close()


    profileInfo = []
    cur.execute("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
    profileInfo = cur.fetchall()
    cur.execute("select name from(person join registration on person.pid = registration.pid) where username = %s", [username])
    personName = cur.fetchone()
    conn.commit()
    cur.close()
=======
    img = fetchone("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [username])

    profileInfo = []
    profileInfo = fetchall("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
    personName = fetchone("select name from(person join registration on person.pid = registration.pid) where username = %s", [username])
>>>>>>> Stashed changes

    return render_template("welcome.html", picture = img, user = username, profileInfo = profileInfo, personName = personName)


@app.route('/createMatch')
def create():

    return render_template("create_match.html", username = username)



@app.route('/findMatch', methods=['GET', 'POST'])
def findMatch():
    global ort
    ort = request.form["ort"]

    show_match.createGame(username)

    return render_template("find_match.html", games=show_match.findGame(ort))



@app.route('/show_games')
def showGame():
    return render_template("show_match.html")

@app.route('/show_match', methods=['GET', 'POST'])
def showMatch():

    ort = request.form["ort"]
    klass = request.form["klass"]
    antal = request.form["antal"]

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


conn.close()
