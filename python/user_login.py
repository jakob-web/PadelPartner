from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padel", 
    user="ak1838",
    password="xrqhw4q4",
    host="pgserver.mah.se")

cur = con.cursor()

@route('/')
def index():
    cur.execute('select namn from person')
    namn = cur.fetchall()
    return template('index.html', namn=namn)

@route('/logIn')
def logIn():

    return template("log_in.html")

@route('logInUser', method="POST")
def logInUser():

    # data regarding the profile table
    userName = request.forms.get("userName")
    password = request.forms.get("pwd")
    print(userName, password)

    def selectMember():
        cur.execute("select * from profile where profile.password = %s", [password])
        

    selectMember()
    
    return template("index.html")

