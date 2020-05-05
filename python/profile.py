from flask import Flask, render_template, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="tennispartner", 
    user="ak3672",
    password="ioczj66l",
    host="pgserver.mah.se")

cur = con.cursor()
def editProfile(username):
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


# def getImg(username):


    
#     cur.execute("select img from(profile join registration on profile.pid = registration.pid) where username = %s", [username])

#     pic = []
#     for record in cur:
#         pic.append(record[0])
#     con.commit()
#     return pic



    # pic = []
    # pic = cur.fetchall()
    # print(pic)
    # img = pic[0]
    # img = ("".join(str(img)))
    # print(img)
    
    # return img


    # img = "select img from(profile join registration on profile.pid = registration.pid) where username = %s"
    # val = username
   
    
    # cur.execute(img, val)
   
    
    


# def getProfile(): 
    
#     sql = "select info, picture from profile"
    


    
