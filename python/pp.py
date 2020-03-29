from bottle import route, run, template, static_file, request, redirect
from os import listdir

import psycopg2

#connect to the db
con = psycopg2.connect( 
    dbname="padel", 
    user="ak3672",
    password="294evcub",
    host="pgserver.mah.se")

cur = con.cursor()

@route('/')
def index():
    cur.execute('select namn from person')
    namn = cur.fetchall()
    return template('index.html')

run(host='localhost', port=8080, debug=True)
con.close()
