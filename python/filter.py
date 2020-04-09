from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

con = psycopg2.connect( 
    dbname="padelpartner", 
    user="ak1838",
    password="xrqhw4q4",
    host="pgserver.mah.se")

cur = con.cursor()

def matchning():
    cur.execute("select username from (profile join registration on profile.pid = registration.pid) where ORT = '%s'")
    cur.fetchall()
    con.commit()
    
        