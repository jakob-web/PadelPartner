from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padel", 
    user="ak3672",
    password="294evcub",
    host="pgserver.mah.se")

cur = con.cursor()



#current table = profiletest // change this later!



def password():
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
                    print("hej")
                    return template("welcome.html", user = username)
                else:
                    print("Felaktigt lösenord eller Användarnamn")
                    redirect("/log_in")
        else:
            redirect("/log_in")

Detta är den nya

con.close()

