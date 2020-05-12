from flask import Flask, render_template, request, redirect
import psycopg2
from config import *
from db_operations import fetchone, fetchmany, fetchall, insert

con = psycopg2.connect( 
    dbname=dbname, 
    user=user,
    password=password,
    host=host)
cur = con.cursor()
def create_Game(username):
    ort = request.form["ort"]
    klass = request.form["klass"]
    antal = request.form["antal"]
    info = request.form["info"]
    datum = request.form["datum"]
    username = request.form["username"]

    sql = "insert into match(ort, klass, antal, info, skapare, booked, datum) values(%s, %s, %s, %s, %s, %s, %s)"
    booked = 4 - int(antal)
    val = ort, klass, antal, info, username, booked, datum
    cur.execute(sql, val)
    con.commit()

def find_Game(ort):
    cur.execute("select ort, klass, antal, matchid from match where ort = %s", [ort])
    
    games = []
    for record in cur:
        games.append(record)
    return games

def show_Game(ort,klass,antal):
    print(ort,klass,antal)
    # check if creator name is username session, then don't show.
    sql = "select ort, klass, antal, match.matchid, match.booked from(match join booking on match.matchid = booking.matchid) where ort = %s AND klass = %s AND antal = %s AND antal > 0;"
    val = ort, klass, antal
    games = fetchall(sql, val)
    return games
  

def show_Match_Profile(matchid):
    
    cur.execute("select ort, klass, antal, info, skapare, matchid from match where matchid = %s AND antal > 0", [matchid])
    
    match = []

    for record in cur:
        match.append(record)
    return match

def show_all_match(ort):
    sql = "select ort, klass, antal, matchid from match where ort = %s AND antal > 0"
    val = (ort,)
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games

def show_all_ranks(ort, klass):
    sql = "select ort, klass, antal, matchid from match where ort = %s and klass = %s AND antal > 0"
    val = (ort, klass,)
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games

def show_all_players(ort, antal):
    sql = "select ort, klass, antal, matchid from match where ort = %s and antal = %s AND antal > 0"
    val = (ort, antal,)
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games
    

   

    
  
        