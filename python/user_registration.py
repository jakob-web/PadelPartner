from flask import Flask, render_template, request
import hashlib, binascii, os
from db_operations import insert, fetchall

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def register():
    """
    Receives User registration information from a form and creates Person,Profile % registartion in the database.
    """
    fName = request.form["fName"]
    lName = request.form["lName"]
    email = request.form["email"]
    gender = request.form["gender"]

    username = request.form["userName"]
    password = request.form["pwd"]
    password = hash_password(password)

    level = request.form["level"]
    location = request.form["location"]

    username_list = fetchall("select username from registration", "")
    username_list = ("".join(str(username_list)))
    
    if username not in username_list:
        def insert_person():
            sql = "insert into person(name, email, gender) values(%s,%s,%s)"
            name = fName + " " + lName
            val = (name, email, gender,)
            insert(sql,val)

        def insert_registration():
            sql = "insert into registration(username, password) values(%s,%s)"
            val = (username, password,)
            insert(sql,val)

        def insert_profile():
            sql = "insert into profile(img, level, location) values(%s, %s, %s)"
            image = 'static/img/uploads/blank_profile.png'
            val = (image, level, location)
            insert(sql,val)

        insert_person()
        insert_profile()
        insert_registration()
        return True
    else:
        return False
