from flask import Flask, render_template, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padelpart", 
    user="aj9613",
    password="g0rvfpok",
    host="pgserver.mah.se")
    
cur = con.cursor()
#TODO BUG, Skapa match och gå sedan ett steg tillbaka så skapas match igen & igen.....

def createGame(username):
    ort = request.form["ort"]
    klass = request.form["klass"]
    antal = request.form["antal"]
    info = request.form["info"]
    username = request.form["username"]
    

    

    sql = "insert into match(ort, klass, antal, info, skapare) values(%s, %s, %s, %s, %s)"
    val = ort, klass, antal, info, username
    cur.execute(sql, val)
    con.commit()

def findGame(ort):
    cur.execute("select ort, klass, antal, matchid from match where ort = %s", [ort])
    
    games = []
    for record in cur:
        games.append(record)
    return games

def showGame(ort,klass,antal):
    print(ort,klass,antal)
    # cur.execute("select ort, klass, antal, matchid from match where ort = %s AND klass = %s AND antal = %s", [ort],[klass],[antal])
    sql = "select ort, klass, antal, matchid from match where ort = %s AND klass = %s AND antal = %s"
    val = ort, klass, antal
    cur.execute(sql, val)
    games = []
    for record in cur:
        games.append(record)
    return games

def showMatchProfile(matchid):
    
    cur.execute("select ort, klass, antal, info, skapare from match where matchid = %s", [matchid])
    
    match = []

    for record in cur:
        match.append(record)
        
    return match


     
# def showGame():
#     cur.execute("select ort, klass from match where ort = %s", [ort])


    # games = cur.execute(sql, val)
    # con.commit()
    


   

    
  
        