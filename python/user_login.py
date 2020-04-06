from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padel", 
    user="ak3672",
    password="294evcub",
    host="pgserver.mah.se")

cur = con.cursor()


def login():
    cred = []
    cur.execute("select username from profile")
    cred = cur.fetchall()
    usernameList = ("".join(str(cred)))
    print(usernameList)
    username = getattr(request.forms, "userName")
    password = getattr(request.forms, "pwd")
    
    if username in usernameList:
        print("YES1")
        cur.execute("select password from profile where username='%s'" % (username))
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
