from flask import Flask, render_template, request, redirect
import hashlib, binascii, os
from config import *
import psycopg2
from flask import flash


con = psycopg2.connect( 
    dbname=dbname, 
    user=user,
    password=password,
    host=host)

cur = con.cursor()

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def register():
    """
    Receives User resitration information from a form and creates Person & Profile in the database.
    """
    level = request.form["level"]

    förnamn = request.form["fNamn"]
    efternamn = request.form["eNamn"]
    email = request.form["email"]
    gender = request.form["gender"]

    userName = request.form["userName"]
    password = request.form["pwd"]
    password = hash_password(password)

    level = request.form["level"]
    ort = request.form["ort"]
    
    cur.execute('select username from registration')
    usernameList = cur.fetchall()
    usernameList = ("".join(str(usernameList)))

    if userName not in usernameList:
        def insert_Person():
            sql = "insert into person(name, email, gender) values(%s,%s,%s)"
            namn = förnamn + " " + efternamn
            val = namn, email, gender
            cur.execute(sql,val)
            con.commit()
            
        def insert_Registration():
            sql = "insert into registration(username, password) values(%s,%s)"
            val = userName,password
            cur.execute(sql,val)
            con.commit()

        def insert_Profile():
            sql = "insert into profile(img, level, ort) values(%s, %s, %s)"
            image = '/static/blank_profile.png'
            val = image, level, ort
            cur.execute(sql, val)
            con.commit()

        insert_Person()
        insert_Profile()
        insert_Registration()
        return True
    else: 
        return False