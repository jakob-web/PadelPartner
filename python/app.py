from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
from flask import flash
from os import listdir
import main
import user_registration
import user_login
import profile
import show_match
import psycopg2
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
con = psycopg2.connect( 
    dbname="padelpar", 
    user="ak1838",
    password="xrqhw4q4",
    host="pgserver.mah.se")

cur = con.cursor()

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
        flash("Fel lösenord eller användarnamn")
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

@app.route('/show_past_chatt')
def showPastChatt():
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
def showChatt(matchid):
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
