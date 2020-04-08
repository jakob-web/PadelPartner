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
    cur.execute("select max(id) from profile1")
    for row in cur:
        id=row[0]
        id=id+1
    img = getattr(request.forms, "img")
    info = getattr(request.forms, "info")
    sql = "insert into profile1 values (%s, %s, %s)"
    val = id, info, img
    cur.execute(sql, val)
    con.commit()

def getProfile(): 
    
    sql = "select info, picture from profile"
    


    
