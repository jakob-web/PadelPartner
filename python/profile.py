from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padelpartner", 
    user="ak1838",
    password="xrqhw4q4",
    host="pgserver.mah.se")

cur = con.cursor()
def editProfile():
    # cur.execute("select max(id) from profile1")
    # for row in cur:
    #     id=row[0]
    #     id=id+1
    img = getattr(request.forms, "img")
    info = getattr(request.forms, "info")
    level = getattr(request.forms, "level")
    age = getattr(request.forms, "age")
    sql = "update profile set img = %s, info = %s, level = %s, age = %s" 
    val = img, info, level, age
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
    


    
