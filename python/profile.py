from flask import Flask, render_template, request, redirect
import psycopg2

con = psycopg2.connect( 
    dbname="padelpar", 
    user="ak0153",
    password="uv93mszx",
    host="pgserver.mah.se")

cur = con.cursor()
def edit_Profile(username):
    img = request.form["img"]
    info = request.form["info"]
    level = request.form["level"]
    age = request.form["age"]
    cur.execute("select pid from registration where username = %s", [username])
    asd = cur.fetchone()
    sql = "update profile set img = %s, info = %s, level = %s, age = %s where pid = %s" 
    val = img, info, level, age, asd
    cur.execute(sql, val)
    con.commit()



    


    
