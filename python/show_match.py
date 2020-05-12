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
    kön = request.form["kön"]
    username = request.form["username"]

    sql = "insert into match(ort, klass, antal, info, skapare, booked, datum, kön) values(%s, %s, %s, %s, %s, %s, %s, %s)"
    booked = 4 - int(antal)
    val = ort, klass, antal, info, username, booked, datum, kön
    
    cur.execute(sql, val)
    con.commit()

def find_Game(ort):
    cur.execute("select ort, klass, antal, matchid, kön from match where ort = %s", [ort])
    
    games = []
    for record in cur:
        games.append(record)
    print(games)
    return games

def show_Game(ort,klass,kön):
    print(ort,klass,kön)
    sql = "select ort, klass, antal, matchid, kön, datum from match where ort = %s AND klass = %s AND kön = %s AND antal > 0;"
    val = ort, klass, kön
    games = fetchall(sql, val)
    return games
  

def show_Match_Profile(matchid):
    
    result = fetchall("select ort, klass, antal, info, skapare, matchid, kön from match where matchid = %s AND antal > 0", [matchid])
    
    match = []
    print(match)
    for record in result:
        match.append(record)
    
    return match

def show_all_match(ort):
    print(ort)
    result = fetchall("select ort, klass, antal, matchid, kön, datum from match where ort = %s AND antal > 0", [ort])
    # sql = "select ort, klass, antal, matchid, kön, datum from match where ort = %s AND antal > 0"
    # val = ort
    # result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)

    return games

def show_all_ranks(ort, klass):
    sql = "select ort, klass, antal, matchid, kön, datum from match where ort = %s and klass = %s AND antal > 0"
    val = (ort, klass)
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games

def show_all_players(ort, kön):
    print(kön)
    sql = "select ort, klass, antal, matchid, kön, datum from match where ort = %s and kön = %s AND antal > 0"
    val = (ort, kön)
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games
    

   

    
  
        