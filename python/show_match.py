from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padelpart", 
    user="ak0153",
    password="uv93mszx",
    host="pgserver.mah.se")

cur = con.cursor()

def createGame(username):
    ort = getattr(request.forms, "ort")
    klass = getattr(request.forms, "klass")
    antal = getattr(request.forms, "antal")
    info = getattr(request.forms, "info")
    username = getattr(request.forms, "username")
    

    

    sql = "insert into match(ort, klass, antal, info, skapare) values(%s, %s, %s, %s, %s)"
    val = ort, klass, antal, info, username
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

def showMatchProfile(username, ort):
   
    cur.execute("select ort, klass, antal, info, skapare from match where skapare = %s AND ort = %s",[username, ort])
    match = []
    
    for record in cur:
        match.append(record)
    return match


     
# def showGame():
#     cur.execute("select ort, klass from match where ort = %s", [ort])


    # games = cur.execute(sql, val)
    # con.commit()
    


   

    
  
        