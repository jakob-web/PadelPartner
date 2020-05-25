from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_socketio import SocketIO, send
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

    players = request.form["players"]

    show_match.create_Game(session["username"])
    matchid = fetchone("select max(matchid) from match where matchid > %s", "0")
    if matchid[0] == None:
        matchid = 1
    sql = "insert into booking (matchid,username,creatorname,booked) values (%s,%s,%s,%s)"
    val = matchid,session["username"],session["username"],players
    insert(sql, val)

    return start_page()


@app.route('/show_games')
def show_game():
    
    return render_template("show_match.html")

@app.route('/show_match', methods=['GET', 'POST'])
def show_matches():
    
    location = request.form["location"]
    level = request.form["level"]
    gender = request.form["gender"]
    
    games = show_match.main_show(location,level,gender)
    return render_template("find_match.html", games=games)

@app.route('/showMatchProfile/<matchid>')
def show_match_profile(matchid):    
    matchid = matchid
    result = fetchall("select location, level, info, creator, matchid, players from match where matchid = %s", [matchid])
    my_matches = []
    for record in result:
        my_matches.append(record)
    return render_template("match_profile.html", match = show_match.show_Match_Profile(matchid), my_matches = my_matches)

@app.route('/my_games/')
def show_my_games():
    show_match.check_date()
    game = fetchall("select location, level, players, creator, match.matchid, date, gender from (match join booking on match.matchid = booking.matchid) where booking.username = %s ORDER BY date;", [session["username"]])
    return render_template("my_games.html", user = session["username"], matches = game)

@app.route('/my_games_info/<matchid>')
def my_game_info(matchid):
    matchid = matchid
    result = fetchall("select location, level, info, creator, matchid, players from match where matchid = %s", [matchid])
    my_matches = []
    for record in result:
        my_matches.append(record)
        
    #Checks if creator = username
    if my_matches[0][3] == session["username"]:
        return render_template("show_my_games.html", user = session["username"], my_matches = my_matches, creator = True, comments = show_comment(matchid))
    else:
        return render_template("show_my_games.html", user = session["username"], my_matches = my_matches, comments = show_comment(matchid))

@app.route('/remove_match/<matchid>')
def remove_match(matchid):
    update("delete from match where matchid = %s",[matchid])
    update("delete from booking where matchid = %s",[matchid])
    return show_my_games()
    
@app.route('/remove_booking/<matchid>')
def remove_booking(matchid):
    sql = "select booked from booking where matchid=%s AND username=%s"
    val = matchid, session["username"]
    current_booking = fetchone(sql,val) 

    sql = "update match set players=(players+%s) where matchid =%s"
    val = current_booking,matchid
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
    return render_template("messages.html", user = session["username"], messages = messages)

@app.route('/book_game/<matchid>', methods=['GET', 'POST'])
def booking_game(matchid):
    matchid = int(matchid)
    players = request.form["players"]
    print(players)
    if players == "0":
        flash("Var vänlig och boka en plats")
        print("players = 0" + players)
        return render_template("match_profile.html", match = show_match.show_Match_Profile(matchid))

    else:
        print("antal högre än 0:" + players)
        booked = fetchone("select booked from match where matchid = %s", [matchid])
        def new_booked():
            print(players)
            if (int(players) + booked[0]) > 4:
                return "4"
            else:
                return int(players) + booked[0]

            print(matchid, session["username"])

        creatorName = fetchone("select creator from match where matchid = %s", [matchid])
        sql = "insert into booking values(%s,%s,%s,%s)"
        val = matchid,session["username"],creatorName,players
        insert(sql, val)

        sql = "UPDATE match SET booked = %s WHERE matchid = %s;"
        val = new_booked(),matchid
        update(sql, val)
        
        sql = "UPDATE match SET players = %s WHERE matchid = %s;"
        searching = fetchone("select players from match where matchid = %s", [matchid])
        print(searching[0])
        searching = searching[0] - int(players)
        val = searching,matchid
        update(sql, val)

        return start_page()
    
    sql = "UPDATE match SET players = %s WHERE matchid = %s;"
    searching = fetchone("select players from match where matchid = %s", [matchid])
    print(searching[0])
    searching = searching[0] - int(players)
    val = searching,matchid
    update(sql, val)

    return start_page()
   
@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

@app.route('/uploadpicture', methods=['GET', 'POST'])
def uploadpicture():
    return render_template("uploadpicture.html")

@app.route('/testRoute', methods=['GET'])
def uploadpictureok():
    return "Hello world"

@app.route('/creator_profile/<creator>')
def creator_profile(creator):
    creator = creator
    profil = fetchall("select profile.info, profile.level, profile.age, profile.location FROM((Match join registration on Match.creator = registration.username)join profile on registration.pid = profile.pid) WHERE creator = %s", [creator])
    img = fetchall("select profile.img FROM((Match join registration on Match.creator = registration.username)join profile on registration.pid = profile.pid) WHERE creator = %s", [creator])
    print(profil)
    print(img)

    return render_template("creator_profile.html", creator = creator, profil = profil, img = img)

@app.route('/change_password/')
def new_password():
    return render_template("change_password.html")

@app.route('/new_password', methods=['GET', 'POST'])
def check_password():
    password = request.form["pwd"]
    new_password = request.form["new_pwd"]
    result = profile.change_password(password, new_password)
    
    if result == True:
        return start_page()
    elif result == False:
        return render_template("change_password.html")


@app.route('/make_comment/<matchid>', methods=['GET', 'POST'])
def new_comment(matchid):
    comment = request.form["comment"]
    matchid = matchid
    sql = "insert into msg(writer, message, matchid) VALUES (%s, %s, %s)"
    val = session["username"], comment, matchid
    insert(sql, val)
    return my_game_info(matchid)

def show_comment(matchid):
    print("hej")
    matchid = matchid
    result = fetchall("select message, writer, matchid from msg where matchid = %s ORDER BY date DESC", [matchid])
    print(result)
    comments = []
    for record in result:
        print(record)
        comments.append(record)
    print(comments)
    return comments


# Future chatt fnction
# @app.route('/show_chatt')
# def show_chats():
#     return render_template("session.html")
    
# @socketio.on('message')
# def handleMessage(msg):
#     print('Message: ' + msg)
#     send(msg, broadcast=True)




# @socketio.on('message')
# def handleMessage(msg):
# 	print('Message: ' + msg)
# 	send(msg, broadcast=True)




if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8080, debug=True)
    socketio.run(app, debug=True)
