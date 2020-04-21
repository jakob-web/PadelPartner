from bottle import route, run, template, static_file, request, redirect
from os import listdir
import hashlib, binascii, os
import psycopg2
import hashlib, binascii, os

con = psycopg2.connect( 
    dbname="padelpart", 
    user="ak0153",
    password="uv93mszx",
    host="pgserver.mah.se")

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
    level = getattr(request.forms,"level")

    # data regarding the person table
    förnamn = getattr(request.forms,"fNamn")
    efternamn = getattr(request.forms,"eNamn")
    email = getattr(request.forms,"email")
    gender = getattr(request.forms,"gender")
    print(förnamn, efternamn, email, gender)

    # data regarding the registration table
    userName = getattr(request.forms,"userName")
    password = getattr(request.forms,"pwd")
    print(userName, password)
    password = hash_password(password)
    print(password)

    level = getattr(request.forms,"level")
    ort = getattr(request.forms, "ort")
    #Convert password to hash
    password = hash_password(password)

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
            sql = "insert into profile(level, ort) values(%s, %s)"
            val = level, ort
            cur.execute(sql, val)
            con.commit()

        insertPerson()
        insertProfile()
        insertRegistration()
        return True
    else: 
        return False