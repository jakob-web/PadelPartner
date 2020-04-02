from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padel", 
    user="aj9613",
    password="g0rvfpok",
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

@route('/logInUser', method="POST")
def logInUser():
    print("hej")
    # data regarding the profile table
    userName = getattr(request.forms,"userName")
    password = getattr(request.forms,"password")
    print(userName, password)

   

    def selectMember():
        userSelect = []
        userSelect.append(userName)
        userSelect.append(password)
        
        sql = "select * from profile where username = %s AND profile.password = %s"
        cur.execute(sql, userSelect)
        

    selectMember()
    
    return template("welcome.html")


run(host='localhost', port=8080, debug=True)
con.close()

