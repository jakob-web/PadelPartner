from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
from flask import flash
import main
import user_registration
import user_login
import profile
import show_match
from config import *
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
con = psycopg2.connect( 
    dbname=dbname, 
    user=user,
    password=password,
    host=host)

cur = con.cursor()

username = ''
img = ''

@app.route('/test')
def test():
    return render_template('test.html', user = session["username"])

@app.route('/')
def index():
    return render_template('log_in.html', username = username)

@app.route('/logIn')
def log_in():
    return render_template('log_in.html', username = username)

@app.route('/register')
def register_form():
    """
    Shows a form for registration of a user.
    """
    return render_template("user_registration.html")

@app.route('/registerUser' , methods=['GET', 'POST'])
def register_user():
    if user_registration.register() == True:
        return render_template("log_in.html",username="")

    elif user_registration.register() == False:
        flash("Användarnamn existerar redan")
        return render_template("user_registration.html")


@app.route('/logInUser', methods=['GET', 'POST'])
def user_log():
    if user_login.log_in() == True:
        global username
        username = request.form["userName"]
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
        session["username"] = username
        return render_template("welcome.html", picture = img, user = session["username"], profileInfo = profileInfo, personName = personName)
        
    elif user_login.log_in() == False:
        flash("Fel lösenord eller användarnamn")
        return render_template("log_in.html", username = "")


@app.route('/changeProfile')
def change_profile():
    cur.execute("select * from (profile join registration on profile.pid = registration.pid) where username = %s", [username])
    informationProfile = cur.fetchall()
    print(informationProfile)
    return render_template("edit_profile.html",user = username, info = informationProfile)

@app.route('/profile', methods=['GET', 'POST'])
def profil():
    global username
    profile.edit_Profile(username)
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
    global username 
    
    matchid = matchid
    return render_template("match_profile.html", match = show_match.show_Match_Profile(matchid))

@app.route('/show_past_chatt')
def show_past_chatt():
    global username
    print(username)
    messages = []
    sql = "select writer,message,date from msg WHERE writer = %s OR reciever = %s"
    val = username, username
    cur.execute(sql, val)
    messages = cur.fetchall()
    print(messages)
    return render_template("messages.html", user = username, messages = messages)


@app.route('/show_chatt/<matchid>', methods=['GET', 'POST'])
def show_chatt(matchid):
    global username 
    matchid = int(matchid)
    print(matchid, username)
    cur.execute("select skapare from match where matchid = %s", [matchid])
    creatorName = cur.fetchone()
    sql = "insert into booking values(%s,%s,%s)"
    val = matchid,username,creatorName
    print(matchid, username,creatorName)
    cur.execute(sql,val)
    con.commit()

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


con.close()
