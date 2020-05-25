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
    Converts database "date" to same format as date.today() and compares if the date is expired.
    If date expired = remove match from database.
    """
    current = date.today()
    current = current.strftime("%a, %d %b %Y")
    current = datetime.strptime(str(current), "%a, %d %b %Y")
    result = fetchall("select date from match where matchid > %s", [0])
    print(current)
    
    for record in result:
        record = datetime.strptime(record[0], "%a, %d %b %Y")
        if record < current:
            print("delete")
            new_record = record.strftime("%a, %d %b %Y")
            print(new_record)
            update("delete from match where date = %s",[new_record])

def main_show(location,level,gender):
    """
    Checks which parts of the form that are checked.

    1. Check if the list of games that are returned contains the same username  as sessions[username].
    2. Checks if any of the matches in the list are dulpicated by comparing them to the list.
    If that's the case it does'nt append the match to the new list.
    """
    if level == "1" and gender !="6":
        games = show_all_players(location, gender)
    elif level != "1" and gender =="6":
        games = show_all_ranks(location, level)
    elif level == "1" and gender =="6":
        games = show_all_match(location)
    else:
        games = show_Game(location,level,gender)



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
    location = request.form["location"]
    level = request.form["level"]
    players = request.form["players"]
    info = request.form["info"]
    date = request.form["date"]
    gender = request.form["gender"]
    username = request.form["username"]

    sql = "insert into match(location, level, players, info, creator, booked, date, gender) values(%s, %s, %s, %s, %s, %s, %s, %s)"
    booked = 4 - int(players)
    val = location, level, players, info, username, booked, date, gender
    
    cur.execute(sql, val)
    con.commit()



def show_Game(location,level,gender):
    check_date()
    sql = "select DISTINCT location,level,players,match.matchid,gender,date,username from (match join booking on match.matchid = booking.matchid) where location = %s AND level = %s AND gender = %s AND players > 0 AND skapare != %s ORDER BY date"
    val = location, level, gender, session["username"]
    games = fetchall(sql, val)
    return games
  

def show_Match_Profile(matchid):
    result = fetchall("select location, level, players, info, creator, matchid, gender from match where matchid = %s AND players > 0", [matchid])
    
    match = []
    for record in result:
        match.append(record)
    return match



def show_all_match(location):
    check_date()
    sql = "select DISTINCT location,level,players,match.matchid,gender,date,username from (match join booking on match.matchid = booking.matchid) WHERE location = %s AND players > 0 AND skapare != %s ORDER BY date"

    val = (location, session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games
    

def show_all_ranks(location, level):
    check_date()
    sql = "select DISTINCT location,level,players,match.matchid,gender,date,username from (match join booking on match.matchid = booking.matchid) where location = %s and level = %s AND players > 0 AND skapare != %s ORDER BY date"
    val = (location, level,session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    return games

def show_all_players(location, gender):
    check_date()
    print(gender)
    sql = "select DISTINCT location,level,players,match.matchid,gender,date,username from (match join booking on match.matchid = booking.matchid) where location = %s and gender = %s AND players > 0 AND skapare != %s ORDER BY date"
    val = (location, gender,session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    return games
    

   

    
  
        