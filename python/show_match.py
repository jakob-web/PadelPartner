from flask import Flask, render_template, request, redirect
from os import listdir
from db_operations import insert, fetchall

import psycopg2



#TODO BUG, Skapa match och gå sedan ett steg tillbaka så skapas match igen & igen.....

def create_Game(username):
    ort = request.form["ort"]
    klass = request.form["klass"]
    antal = request.form["antal"]
    info = request.form["info"]
    username = request.form["username"]




    sql = "insert into match(ort, klass, antal, info, skapare) values(%s, %s, %s, %s, %s)"
    val = (ort, klass, antal, info, username,)
    insert(sql, val)

def find_Game(ort):
    result = fetchall("select ort, klass, antal, matchid from match where ort = %s", [ort])

    games = []
    for record in result:
        games.append(record)
    return games

def show_Game(ort,klass,antal):
    print(ort,klass,antal)
    sql = "select ort, klass, antal, matchid from match where ort = %s AND klass = %s AND antal = %s"
    val = (ort, klass, antal,)
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    return games

def show_Match_Profile(matchid):

    result = fetchall("select ort, klass, antal, info, skapare, matchid from match where matchid = %s", [matchid])

    match = []

    for record in result:
        match.append(record)
    return match

def show_all_match(ort):
    sql = "select ort, klass, antal, matchid from match where ort = %s"
    val = (ort,)
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    return games

def show_all_ranks(ort, klass):
    sql = "select ort, klass, antal, matchid from match where ort = %s and klass = %s"
    val = (ort, klass,)
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    return games

def show_all_players(ort, antal):
    sql = "select ort, klass, antal, matchid from match where ort = %s and antal = %s"
    val = (ort, antal,)
    result = fetchall(sql, val)
    games = []
    for record in result:
        games.append(record)
    return games
    

   

    
  
        
