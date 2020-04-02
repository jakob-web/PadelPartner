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

@route('/register')
def register_form():
    """
    Shows a form for registration of a user.
    """
    return template("user_registration.html")

@route('/registerUser', method="POST")
def register():
    """
    Receives User resitration information from a form and creates Person & Profile in the database.
    """

    # data regarding the person table
    förnamn = request.forms.get("fNamn")
    efternamn = request.forms.get("eNamn")
    pnr = request.forms.get("pnr")
    level = request.forms.get("level")
    info = request.forms.get("info")
    print(förnamn, efternamn, pnr, level, info)
    
    # data regarding the profile table
    userName = request.forms.get("userName")
    password = request.forms.get("pwd")
    print(userName, password)

    # fetches the current highest id num and adds 1
    cur.execute("select max(id) from profile")
    for row in cur:
        id=row[0]
        id=id+1

    def insertPerson():
        sql = "insert into person values(%s,%s,%s,%s)"
        namn = förnamn + " " + efternamn
        val = pnr,namn,level,info
        cur.execute(sql,val)
        con.commit()
        
    def insertProfile():
        sql = "insert into profile values(%s,%s,%s)"
        val = id,userName,password
        cur.execute(sql,val)
        con.commit()

    insertPerson()
    insertProfile()


    return template("user_registration.html")


run(host='localhost', port=8080, debug=True)
con.close()
