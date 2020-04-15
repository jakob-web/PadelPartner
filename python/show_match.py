from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padelpart", 
    user="aj9613",
    password="g0rvfpok",
    host="pgserver.mah.se")

cur = con.cursor()

def createGame():
    ort = getattr(request.forms, "ort")
    klass = getattr(request.forms, "klass")
    antal = getattr(request.forms, "antal")
    info = getattr(request.forms, "info")

    

    sql = "insert into match(ort, klass, antal, info) values(%s, %s, %s, %s)"
    val = ort, klass, antal, info
    cur.execute(sql, val)
    con.commit()

def findGame(ort):
    cur.execute("select ort, klass, antal from match where ort = %s", [ort])
    
    games = []
    for record in cur:
        games.append(record)
    return games

def showGame(ort):
    cur.execute("select ort, klass, antal from match where ort = %s", [ort])

    games = []
    for record in cur:
        games.append(record)
    return games

# def showMatchProfile():

    # cur.execute("select ")
    # return .-...


    #  if userName not in usernameList:
    
    #     def insertPerson():
    #         sql = "insert into person(name, email, gender) values(%s,%s,%s)"
    #         namn = förnamn + " " + efternamn
    #         val = namn, email, gender
    #         cur.execute(sql,val)
    #         con.commit()
            
    #     def insertRegistration():
    #         sql = "insert into registration(username, password) values(%s,%s)"
    #         val = userName,password
    #         cur.execute(sql,val)
    #         con.commit()

    #     def insertProfile():
    #         sql = "insert into profile(level, ort) values(%s, %s)"
    #         val = level, ort
    #         cur.execute(sql, val)
    #         con.commit()

    #     insertPerson()
    #     insertProfile()
    #     insertRegistration()
    #     return True
    # else: 
    #     return False

# def showGame():
#     cur.execute("select ort, klass from match where ort = %s", [ort])


    # games = cur.execute(sql, val)
    # con.commit()
    


   

    
  
        