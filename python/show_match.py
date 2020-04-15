from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padelpartner", 
    user="ak1838",
    password="xrqhw4q4",
    host="pgserver.mah.se")

cur = con.cursor()

def createGame():
    ort = getattr(request.forms, "ort")
    klass = getattr(request.forms, "klass")
    antal = getattr(request.forms, "antal")
    

    sql = "insert into match(ort, klass, antal) values(%s, %s, %s)"
    val = ort, klass, antal
    cur.execute(sql, val)
    con.commit()

def findGame(ort):
    
    sql ="select matchID from match where ort = %s", [ort]
    val = ort
    games = cur.execute(sql, val)
    con.commit()
    return games
    
  
        