from flask import Flask, render_template, request, redirect
from os import listdir
import hashlib, binascii, os
import psycopg2

con = psycopg2.connect( 
    dbname="padelpartner", 
    user="jakob",
    password="bokaj",
    host="127.0.0.1")

cur = con.cursor()

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    print(pwdhash)
    return (salt + pwdhash).decode('ascii')

def register():
    """
    Receives User resitration information from a form and creates Person & Profile in the database.
    """

    # data regarding the profile table
    level = request.form["level"]

    # data regarding the person table
    förnamn = request.form["fNamn"]
    efternamn = request.form["eNamn"]
    email = request.form["email"]
    gender = request.form["gender"]
    print(förnamn, efternamn, email, gender)

    # data regarding the registration table
    userName = request.form["userName"]
    password = request.form["pwd"]
    print(userName, password)
    password = hash_password(password)
    print(password)

    level = request.form["level"]
    ort = request.form["ort"]
    


    # if user name doesn't already exists
    cur.execute('select username from registration')
    usernameList = cur.fetchall()
    usernameList = ("".join(str(usernameList)))
    print(usernameList)
    if userName not in usernameList:
    
        def insertPerson():
            sql = "insert into person(name, email, gender) values(%s,%s,%s)"
            namn = förnamn + " " + efternamn
            val = namn, email, gender
            cur.execute(sql,val)
            con.commit()
            
        def insertRegistration():
            sql = "insert into registration(username, password) values(%s,%s)"
            val = userName,password
            cur.execute(sql,val)
            con.commit()

        def insertProfile():
            sql = "insert into profile(img, level, ort) values(%s, %s, %s)"
            image = '/static/criminal.jpg'
            val = image, level, ort
            cur.execute(sql, val)
            con.commit()

        insertPerson()
        insertProfile()
        insertRegistration()
        return True
    else: 
        return False