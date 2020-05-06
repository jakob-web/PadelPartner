from flask import Flask, render_template, request, redirect
from os import listdir
from db_operations import insert, fetchall

import psycopg2

<<<<<<< Updated upstream
conn = psycopg2.connect( 
    dbname="padelpar", 
    user="aj7951",
    password="ez2g1c1h",
    host="pgserver.mah.se")
    
cur = conn.cursor()
=======
>>>>>>> Stashed changes
#TODO BUG, Skapa match och gå sedan ett steg tillbaka så skapas match igen & igen.....

def createGame(username):
    ort = request.form["ort"]
    klass = request.form["klass"]
    antal = request.form["antal"]
    info = request.form["info"]
    username = request.form["username"]




    sql = "insert into match(ort, klass, antal, info, skapare) values(%s, %s, %s, %s, %s)"
<<<<<<< Updated upstream
    val = ort, klass, antal, info, username
    cur.execute(sql, val)
    conn.commit()
    cur.close()

def findGame(ort):
    cur.execute("select ort, klass, antal, matchid from match where ort = %s", [ort])
    conn.commit()
    cur.close()
    
=======
    val = (ort, klass, antal, info, username,)
    insert(sql, val)

def findGame(ort):
    result = fetchall("select ort, klass, antal, matchid from match where ort = %s", [ort])

>>>>>>> Stashed changes
    games = []
    for record in result:
        games.append(record)
    return games

def showGame(ort,klass,antal):
    print(ort,klass,antal)
    # cur.execute("select ort, klass, antal, matchid from match where ort = %s AND klass = %s AND antal = %s", [ort],[klass],[antal])
    sql = "select ort, klass, antal, matchid from match where ort = %s AND klass = %s AND antal = %s"
<<<<<<< Updated upstream
    val = ort, klass, antal
    cur.execute(sql, val)
    conn.commit()
    cur.close()
=======
    val = (ort, klass, antal,)
    result = fetchall(sql, val)
>>>>>>> Stashed changes
    games = []
    for record in result:
        games.append(record)
    return games

def showMatchProfile(matchid):
<<<<<<< Updated upstream
    
    cur.execute("select ort, klass, antal, info, skapare from match where matchid = %s", [matchid])
    conn.commit()
    cur.close()
=======

    result = fetchall("select ort, klass, antal, info, skapare from match where matchid = %s", [matchid])

>>>>>>> Stashed changes
    match = []

    for record in result:
        match.append(record)

    return match

conn.close()


# def showGame():
#     cur.execute("select ort, klass from match where ort = %s", [ort])


    # games = cur.execute(sql, val)
    # con.commit()
