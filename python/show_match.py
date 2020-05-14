from flask import Flask, render_template, request, redirect, session
import psycopg2
from config import *
from db_operations import fetchone, fetchmany, fetchall, insert, update
from datetime import date
from datetime import timedelta  
from datetime import datetime  


con = psycopg2.connect( 
    dbname=dbname, 
    user=user,
    password=password,
    host=host)
cur = con.cursor()

def check_date(): 
    """
    Converts database "datum" to same format as date.today() and compares if the date is expired.
    If date expired = remove match from database.
    """
    current = date.today()
    current = current.strftime("%a, %d %b %Y")
    print(current)
    current = datetime.strptime(str(current), "%a, %d %b %Y")
    result = fetchall("select datum from match where matchid > %s", [0])
    print(current)
    
    for record in result:
        record = datetime.strptime(record[0], "%a, %d %b %Y")
        print(record)
        print(current)
        if record < current:
            print("delete")
            print(record)
            new_record = record.strftime("%a, %d %b %Y")
            print(new_record)
            update("delete from match where datum = %s",[new_record])



  

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



def show_Game(ort,klass,kön):
    check_date()
    print(ort,klass,kön)
    sql = "select ort, klass, antal, matchid, kön, datum from match where ort = %s AND klass = %s AND kön = %s AND antal > 0 AND skapare != %s ORDER BY datum"
    val = ort, klass, kön, session["username"]
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
    check_date()
    
    # result = fetchall("select ort, klass, antal, matchid, kön, datum from match where ort = %s AND antal > 0", [ort])
    sql = "select ort, klass, antal, matchid, kön, datum from match where ort = %s AND antal > 0 AND skapare != %s ORDER BY datum"
    val = (ort, session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)

    return games

def show_all_ranks(ort, klass):
    check_date()
    sql = "select ort, klass, antal, matchid, kön, datum from match where ort = %s and klass = %s AND antal > 0 AND skapare != %s ORDER BY datum"
    val = (ort, klass,session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games

def show_all_players(ort, kön):
    check_date()
    print(kön)
    sql = "select ort, klass, antal, matchid, kön, datum from match where ort = %s and kön = %s AND antal > 0 AND skapare != %s ORDER BY datum"
    val = (ort, kön,session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games
    

   

    
  
        