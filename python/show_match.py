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
    result = fetchall("select date from match where matchid > %s", [0])
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
            update("delete from match where date = %s",[new_record])



  

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
    print(location,level,gender)
    sql = "select location, level, players, matchid, gender, date from match where location = %s AND level = %s AND gender = %s AND players > 0 AND creator != %s ORDER BY date"
    val = location, level, gender, session["username"]
    games = fetchall(sql, val)
    return games
  

def show_Match_Profile(matchid):
    result = fetchall("select location, level, players, info, creator, matchid, gender from match where matchid = %s AND players > 0", [matchid])
    
    match = []
    print(match)
    for record in result:
        match.append(record)
    
    return match

def show_all_match(location):
    check_date()
    
    # result = fetchall("select location, level, players, matchid, gender, date from match where location = %s AND players > 0", [location])
    sql = "select location, level, players, matchid, gender, date from match where location = %s AND players > 0 AND creator != %s ORDER BY date"
    val = (location, session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)

    return games

def show_all_ranks(location, level):
    check_date()
    sql = "select location, level, players, matchid, gender, date from match where location = %s and level = %s AND players > 0 AND creator != %s ORDER BY date"
    val = (location, level,session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games

def show_all_players(location, gender):
    check_date()
    print(gender)
    sql = "select location, level, players, matchid, gender, date from match where location = %s and gender = %s AND players > 0 AND creator != %s ORDER BY date"
    val = (location, gender,session["username"])
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    print(games)
    return games
    

   

    
  
        