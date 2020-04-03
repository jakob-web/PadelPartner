from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padel", 
    user="ak3672",
    password="294evcub",
    host="pgserver.mah.se")

cur = con.cursor()

@route('/')
def index():
    cur.execute('select namn from person')
    namn = cur.fetchall()
    return template('index.html', namn=namn)

@route('/logIn')
def logIn():

    return template("log_in.html", username = "")

@route('/logInUser', method="POST")
def login():
    cred = []
    cur.execute("select username from profiletest")
    cred = cur.fetchall()
    username = getattr(request.forms, "userName")
    password = getattr(request.forms, "pwd")
    for name in cred:
        if username == name[0]:
            cur.execute("select password from profiletest where username='%s'" % (username))
            cred = cur.fetchall()
            for pwd in cred:
                if password == pwd[0]:
                    return template('welcome', username = username)
                else:
                    print("fel lösenord")
                    return template("log_in")
        else:
            pass
@route('/loggedIn')
def loggedIn():
    return template("welcome")


run(host='localhost', port=8080, debug=True)
con.close()