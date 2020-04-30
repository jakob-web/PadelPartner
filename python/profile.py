from flask import Flask, render_template, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padelpar", 
    user="ak0153",
    password="uv93mszx",
    host="pgserver.mah.se")



cur = con.cursor()
def edit_Profile(username):
    # cur.execute("select max(id) from profile1")
    # for row in cur:
    #     id=row[0]
    #     id=id+1
    img = request.form["img"]
    info = request.form["info"]
    level = request.form["level"]
    age = request.form["age"]
    #asd = "select pid from registration where username = %s", [username]
    cur.execute("select pid from registration where username = %s", [username])
    asd = cur.fetchone()
    sql = "update profile set img = %s, info = %s, level = %s, age = %s where pid = %s" 
    val = img, info, level, age, asd
    cur.execute(sql, val)
    con.commit()



    


    
