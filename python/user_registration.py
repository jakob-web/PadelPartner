from flask import Flask, render_template, request, redirect
from os import listdir
import hashlib, binascii, os
from db_operations import insert, fetchall

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
    usernameList = fetchall('select username from registration')
    usernameList = ("".join(str(usernameList)))
    print(usernameList)
    if userName not in usernameList:

        def insertPerson():
            sql = "insert into person(name, email, gender) values(%s,%s,%s)"
            namn = förnamn + " " + efternamn
            val = (namn, email, gender,)
            insert(sql,val)

        def insertRegistration():
            sql = "insert into registration(username, password) values(%s,%s)"
            val = (userName, password,)
            insert(sql,val)

        def insertProfile():
            sql = "insert into profile(img, level, ort) values(%s, %s, %s)"
            image = '/static/criminal.jpg'
            val = (image, level, ort,)
            insert(sql,val)

        insertPerson()
        insertProfile()
        insertRegistration()
        return True
    else:
        return False
