from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padel", 
    user="ak3672",
    password="294evcub",
    host="pgserver.mah.se")

cur = con.cursor()


<<<<<<< Updated upstream

#current table = profiletest // change this later!



def password():
||||||| merged common ancestors


"""@route('/logIn')
def logIn():

    return template("log_in.html", username ="")"""

#current table = profiletest // change this later!


def password():
=======
def login():
>>>>>>> Stashed changes
    cred = []
    cur.execute("select username from profile")
    cred = cur.fetchall()
    usernameList = ("".join(str(cred)))
    print(usernameList)
    username = getattr(request.forms, "userName")
    password = getattr(request.forms, "pwd")
<<<<<<< Updated upstream
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

||||||| merged common ancestors
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
                    redirect('/log_in')
        else:
            redirect('/log_in')

    


run(host='localhost', port=8080, debug=True)
con.close()

=======
    
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
>>>>>>> Stashed changes
