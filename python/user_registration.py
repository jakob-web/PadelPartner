from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padelpartner", 
    user="ak1838",
    password="xrqhw4q4",
    host="pgserver.mah.se")

cur = con.cursor()


def register():
    """
    Receives User resitration information from a form and creates Person & Profile in the database.
    """

    # data regarding the person table
    förnamn = getattr(request.forms,"fNamn")
    efternamn = getattr(request.forms,"eNamn")
    email = getattr(request.forms,"email")
    gender = getattr(request.forms,"gender")
    print(förnamn, efternamn, email, gender)
    
    # data regarding the registration table
    userName = getattr(request.forms,"userName")
    password = getattr(request.forms,"pwd")
    print(userName, password)

    level = getattr(request.forms,"level")
    ort = getattr(request.forms, "ort")

    # if user name doesn't already exists
    cur.execute('select username from registration')
    usernameList = cur.fetchall()
    usernameList = ("".join(str(usernameList)))
    print(usernameList)
    if userName not in usernameList:
    
        def insertPerson():
            sql = "insert into person(name, email, gender) values(%s,%s,%s)"
            namn = förnamn + " " + efternamn
            val = namn, email, gender
            cur.execute(sql,val)
            con.commit()
            
        def insertRegistration():
            sql = "insert into registration(username, password) values(%s,%s)"
            val = userName,password
            cur.execute(sql,val)
            con.commit()

        def insertProfile():
            sql = "insert into profile(level, ort) values(%s, %s)"
            val = level, ort
            cur.execute(sql, val)
            con.commit()

        insertPerson()
        insertProfile()
        insertRegistration()
        return True
    else: 
        return False