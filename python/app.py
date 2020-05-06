from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
from flask import flash
import main
import user_registration
import user_login
import profile
import show_match
from db_operations import fetchone, fetchmany, fetchall, insert

import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/test')
def test():
    return render_template('test.html', user = session["username"])


@app.route('/')
def index():
    print(session.get("username"))
    print(session.get("logged_in"))
    if not session.get("logged_in"):
        print("No username found in session")
        return log_in()
    else:
        print("Success")
        username = session["username"]
        img = fetchone("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [username])

        profileInfo = []
        profileInfo = fetchall("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [username])

        personName = fetchone("select name from(person join registration on person.pid = registration.pid) where username = %s", [username])
        session["logged_in"] = True

        return render_template("welcome.html", picture = img, user = session["username"], profileInfo = profileInfo, personName = personName)
        

@app.route('/logIn')
def log_in():
    return render_template('log_in.html', username = "")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@app.route('/register')
def register_form():
    """
    Shows a form for registration of a user.
    """
    return render_template("user_registration.html")

@app.route('/registerUser' , methods=['GET', 'POST'])
def register_user():
    if user_registration.register() == True:
        return render_template("log_in.html", username="")

    elif user_registration.register() == False:
        flash("Användarnamn existerar redan")
        return render_template("user_registration.html")


@app.route('/logInUser', methods=['GET', 'POST'])
def user_log():
    if user_login.log_in() == True:
        username = request.form["userName"]
        img = fetchone("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [username])
        profileInfo = []
        profileInfo = fetchall("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [username])

        personName = fetchone("select name from(person join registration on person.pid = registration.pid) where username = %s", [username])
        print(personName)
        print(username)
        session["username"] = username
        session["logged_in"] = True
        print(session["username"])

        return render_template("welcome.html", picture = img, user = session["username"], profileInfo = profileInfo, personName = personName)
        
    elif user_login.log_in() == False:
        flash("Fel lösenord eller användarnamn")
        return render_template("log_in.html", username = "")


@app.route('/changeProfile')
def changeProfile():
    informationProfile = fetchall("select * from (profile join registration on profile.pid = registration.pid) where username = %s", [session["username"]])
    print(informationProfile)
    return render_template("edit_profile.html",user = session["username"], info = informationProfile)

@app.route('/profile', methods=['GET', 'POST'])
def profil():
    profile.editProfile(session["username"])
    img = fetchone("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [session["username"]])

    profileInfo = []
    profileInfo = fetchall("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [session["username"]])
    personName = fetchone("select name from(person join registration on person.pid = registration.pid) where username = %s", [session["username"]])

    return render_template("welcome.html", picture = img, user = session["username"], profileInfo = profileInfo, personName = personName)

@app.route('/createMatch')
def create():
    return render_template("create_match.html", username = session["username"])

@app.route('/insert_match', methods=['GET', 'POST'])
def insert_match():
    
    ort = request.form["ort"]
    klass = request.form["klass"]
    antal = request.form["antal"]
    
    show_match.create_Game(session["username"])
    return render_template("find_match.html", games=show_match.show_Game(ort,klass,antal))


@app.route('/show_games')
def show_game():
    return render_template("show_match.html")

@app.route('/show_match', methods=['GET', 'POST'])
def show_matches():
    
    ort = request.form["ort"]
    klass = request.form["klass"]
    antal = request.form["antal"]
    
    return render_template("find_match.html", games=show_match.show_Game(ort,klass,antal))

@app.route('/showMatchProfile/<matchid>')
def show_match_profile(matchid):    
    matchid = matchid
    return render_template("match_profile.html", match = show_match.show_Match_Profile(matchid))

@app.route('/show_past_chatt')
def show_past_chatt():
    messages = []
    sql = "select writer,message,date from msg WHERE writer = %s OR reciever = %s"
    val = session["username"], session["username"]
    insert(sql, val)
    messages = fetchall(sql, val)
    print(messages)
    return render_template("messages.html", user = session["username"], messages = messages)


@app.route('/show_chatt/<matchid>', methods=['GET', 'POST'])
def show_chatt(matchid):
    matchid = int(matchid)
    print(matchid, session["username"])
    creatorName = fetchone("select skapare from match where matchid = %s", [matchid])
    sql = "insert into booking values(%s,%s,%s)"
    val = matchid,session["username"],creatorName
    print(matchid, session["username"],creatorName)
    insert(sql, val)

    def sessions():
        return render_template('session.html')

    def messageReceived(methods=['GET', 'POST']):
        print('message was received!!!')


    @socketio.on('my event')
    def handle_my_custom_event(json, methods=['GET', 'POST']):
        print('received my event: ' + str(json))
        socketio.emit('my response', json, callback=messageReceived)
    return render_template('session.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8080, debug=True)
    socketio.run(app, debug=True)

