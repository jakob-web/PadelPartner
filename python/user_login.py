from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padelpartner", 
    user="ak1838",
    password="xrqhw4q4",
    host="pgserver.mah.se")

cur = con.cursor()


def login():
    cred = []
    cur.execute("select username from registration")
    cred = cur.fetchall()
    usernameList = ("".join(str(cred)))
    print(usernameList)
    username = getattr(request.forms, "userName")
    password = getattr(request.forms, "pwd")
    
    if username in usernameList:
        print("YES1")
        cur.execute("select password from registration where username='%s'" % (username))
        cred = cur.fetchall()
        cred = ("".join(str(cred)))
        if password in cred:
                print("YES2")
                return True
        else:
            print("fel lösenord")
            return False
    else:
        return False
