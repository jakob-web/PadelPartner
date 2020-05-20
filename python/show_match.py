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
    current = datetime.strptime(str(current), "%a, %d %b %Y")
    result = fetchall("select datum from match where matchid > %s", [0])
    
    for record in result:
        record = datetime.strptime(record[0], "%a, %d %b %Y")
        if record < current:
            print("delete")
            new_record = record.strftime("%a, %d %b %Y")
            update("delete from match where datum = %s",[new_record])

def main_show(ort,klass,kön):
    """
    Checks which parts of the form that are checked.

    1. Check if the list of games that are returned contains the same username  as sessions[username].
    2. Checks if any of the matches in the list are dulpicated by comparing them to the list.
    If that's the case it does'nt append the match to the new list.
    """
    if klass == "1" and kön !="6":
        games = show_all_players(ort, kön)
    elif klass != "1" and kön =="6":
        games = show_all_ranks(ort, klass)
    elif klass == "1" and kön =="6":
        games = show_all_match(ort)
    else:
        games = show_Game(ort,klass,kön)



    games1 = []
    games2 = []
    matchidContainer = []
    #TODO Test if it's possbile to make 1 function, add matchid in first if instead.
    for record in games:
        if record[6] != session["username"]:
            games1.append(record)
        else:
            print("if not correct" + record[6] + "adds" + str(record[3]))
            # add matchid to the list
            matchidContainer.append(record[3])
            continue

    for record in games1:
        if record[3] in matchidContainer:
            # games2 doesn't append match if it's already present.
            print("matchid finns redan, tar bort match : " + str(record))
        else:
            # matchid append current matchid because of this the match can't get added twice
            matchidContainer.append(record[3])
            # games2 append the match 
            games2.append(record)
            continue
    return games2    

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
    sql = "select DISTINCT ort,klass,antal,match.matchid,kön,datum,username from (match join booking on match.matchid = booking.matchid) where ort = %s AND klass = %s AND kön = %s AND antal > 0 AND skapare != %s ORDER BY datum"
    val = ort, klass, kön, session["username"]
    games = fetchall(sql, val)
    return games
  

def show_Match_Profile(matchid):
    result = fetchall("select ort, klass, antal, info, skapare, matchid, kön from match where matchid = %s AND antal > 0", [matchid])
    
    match = []
    for record in result:
        match.append(record)
    return match



def show_all_match(ort):
    check_date()
    sql = "select DISTINCT ort,klass,antal,match.matchid,kön,datum,username from (match join booking on match.matchid = booking.matchid) WHERE ort = %s AND antal > 0 AND skapare != %s ORDER BY datum"

    val = (ort, session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games
    

def show_all_ranks(ort, klass):
    check_date()
    sql = "select DISTINCT ort,klass,antal,match.matchid,kön,datum,username from (match join booking on match.matchid = booking.matchid) where ort = %s and klass = %s AND antal > 0 AND skapare != %s ORDER BY datum"
    val = (ort, klass,session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    return games

def show_all_players(ort, kön):
    check_date()
    print(kön)
    sql = "select DISTINCT ort,klass,antal,match.matchid,kön,datum,username from (match join booking on match.matchid = booking.matchid) where ort = %s and kön = %s AND antal > 0 AND skapare != %s ORDER BY datum"
    val = (ort, kön,session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    return games
    

   

    
  
        