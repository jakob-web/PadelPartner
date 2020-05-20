from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_socketio import SocketIO
from flask import flash
import main
import user_registration
import user_login
import profile
import show_match
from db_operations import fetchone, fetchmany, fetchall, insert, update
from datetime import date
from datetime import timedelta  


import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)



@app.route('/start_page')
def start_page():
    print(session.get("username"))
    print(session.get("logged_in"))

    if not session.get("logged_in"):
        print("No username found in session")
        return log_in()
    else:
        print("Success")
        img = fetchone("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [session["username"]])

        profileInfo = []
        profileInfo = fetchall("select * from(profile join registration on profile.pid = registration.pid) where username = %s", [session["username"]])

        personName = fetchone("select name from(person join registration on person.pid = registration.pid) where username = %s", [session["username"]])
        session["logged_in"] = True

        return render_template("welcome.html", picture = img, user = session["username"], profileInfo = profileInfo, personName = personName)
        

@app.route('/')
def index():
    session['logged_in'] = False
    return render_template('log_in.html', username = "")

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
        session["username"] = username
        session["logged_in"] = True
        return render_template("welcome.html", picture = img, user = session["username"], profileInfo = profileInfo, personName = personName)
        
    elif user_login.log_in() == False:
        flash("Fel lösenord eller användarnamn")
        return render_template("log_in.html", username = "")


@app.route('/changeProfile')
def changeProfile():
    informationProfile = fetchall("select * from (profile join registration on profile.pid = registration.pid) where username = %s", [session["username"]])
    img = fetchone("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [session["username"]])
    return render_template("edit_profile.html",user = session["username"], info = informationProfile, pics = img)

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
    dates = []
    for i in range (10):
        current = date.today() + timedelta(days=i)
        current = current.strftime("%a, %d %b %Y")
        dates.append(current)
        i+=1
    return render_template("create_match.html", username = session["username"], dates = dates)

@app.route('/insert_match', methods=['GET', 'POST'])
def insert_match():

    antal = request.form["antal"]

    show_match.create_Game(session["username"])
    matchid = fetchone("select max(matchid) from match where matchid > %s", "0")
    print(matchid)
    if matchid[0] == None:
        matchid = 1
        print(matchid)  
    sql = "insert into booking (matchid,username,creatorname,booked) values (%s,%s,%s,%s)"
    val = matchid,session["username"],session["username"],antal
    insert(sql, val)
    print(matchid, session["username"])

    return start_page()


    

@app.route('/show_games')
def show_game():
    
    return render_template("show_match.html")

@app.route('/show_match', methods=['GET', 'POST'])
def show_matches():
    
    ort = request.form["ort"]
    klass = request.form["klass"]
    kön = request.form["kön"]
    
    games = show_match.main_show(ort,klass,kön)
    return render_template("find_match.html", games=games)

@app.route('/showMatchProfile/<matchid>')
def show_match_profile(matchid):    
    matchid = matchid
    return render_template("match_profile.html", match = show_match.show_Match_Profile(matchid))

@app.route('/my_games/')
def show_my_games():
    show_match.check_date()
    game = fetchall("select ort, klass, antal, skapare, match.matchid, datum, kön from (match join booking on match.matchid = booking.matchid) where booking.username = %s ORDER BY datum;", [session["username"]])
    return render_template("my_games.html", user = session["username"], matches = game)

@app.route('/my_games_info/<matchid>')
def my_game_info(matchid):
    matchid = matchid
    result = fetchall("select ort, klass, info, skapare, matchid, antal from match where matchid = %s", [matchid])
    my_matches = []
    for record in result:
        my_matches.append(record)
        
    #Checks if skapare = username
    if my_matches[0][3] == session["username"]:
        return render_template("show_my_games.html", user = session["username"], my_matches = my_matches, creator = True)
    else:
        return render_template("show_my_games.html", user = session["username"], my_matches = my_matches)

@app.route('/remove_match/<matchid>')
def remove_match(matchid):
    update("delete from match where matchid = %s",[matchid])
    update("delete from booking where matchid = %s",[matchid])
    return show_my_games()
    
@app.route('/remove_booking/<matchid>')
def remove_booking(matchid):
    print(matchid, session["username"])
    sql = "select booked from booking where matchid=%s AND username=%s"
    val = matchid, session["username"]
    current_booking = fetchone(sql,val) 
    print(current_booking)

    sql = "update match set antal=(antal+%s) where matchid =%s"
    val = current_booking,matchid
    print(current_booking,matchid)
    update(sql,val)
    sql = "update match set booked=(booked-%s) where matchid =%s"
    val = current_booking,matchid
    update(sql,val)

    sql = "delete from booking where matchid=%s AND username=%s"
    val = matchid,session["username"]
    update(sql,val)



    return show_my_games()

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
    antal = request.form["antal"]
    print(antal)
    if antal == "0":
        flash("Var vänlig och boka en plats")
        print("antal = 0" + antal)
        return render_template("match_profile.html", match = show_match.show_Match_Profile(matchid))

    else:
        print("antal högre än 0:" + antal)
        booked = fetchone("select booked from match where matchid = %s", [matchid])
        def new_booked():
            print(antal)
            if (int(antal) + booked[0]) > 4:
                return "4"
            else:
                return int(antal) + booked[0]

            print(matchid, session["username"])

        creatorName = fetchone("select skapare from match where matchid = %s", [matchid])
        sql = "insert into booking values(%s,%s,%s,%s)"
        val = matchid,session["username"],creatorName,antal
        insert(sql, val)

        sql = "UPDATE match SET booked = %s WHERE matchid = %s;"
        val = new_booked(),matchid
        print(matchid, session["username"])
        update(sql, val)
        
        sql = "UPDATE match SET antal = %s WHERE matchid = %s;"
        sökes = fetchone("select antal from match where matchid = %s", [matchid])
        print(sökes[0])
        sökes = sökes[0] - int(antal)
        val = sökes,matchid
        update(sql, val)

        return start_page()
    
    
    # Future chatt fnction
    # def sessions():
    #     return render_template('session.html')

    # def messageReceived(methods=['GET', 'POST']):
    #     print('message was received!!!')

    # @socketio.on('my event')
    # def handle_my_custom_event(json, methods=['GET', 'POST']):
    #     print('received my event: ' + str(json))
    #     socketio.emit('my response', json, callback=messageReceived)
    # return render_template('session.html')

    
   
@app.route('/about_us')
def about_us():
    
    return render_template("about_us.html")

@app.route('/uploadpicture', methods=['GET', 'POST'])
def uploadpicture():

    return render_template("uploadpicture.html")

@app.route('/testRoute', methods=['GET'])
def uploadpictureok():
    return "hejhejmarcus"


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8080, debug=True)
    socketio.run(app, debug=True)
