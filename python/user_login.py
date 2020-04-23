from bottle import route, run, template, static_file, request, redirect
from os import listdir
import hashlib, binascii, os

import psycopg2

con = psycopg2.connect( 
    dbname="tennispartner", 
    user="ak3672",
    password="294evcub",
    host="pgserver.mah.se")

cur = con.cursor()

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    print("input password " + pwdhash)
    print("Stored password " + stored_password)
    if pwdhash == stored_password:
        return True
    else:
        return False

# #rename 'cred' to stored_password
# stored_password = password
# # remove if password in cred and instead:
# verify_password(stored_password,povided_password)

def login():
    cred = []
    cur.execute("select username from registration")
    cred = cur.fetchall()
    usernameList = ("".join(str(cred)))
    username = getattr(request.forms, "userName")
    password = getattr(request.forms, "pwd")
    
    if username in usernameList:
        print("Username exists")
        cur.execute("select password from registration where username='%s'" % (username))
        cred = cur.fetchone()
        stored_password = cred[0]
        if verify_password(stored_password,password):
                print("Password is correct")
                return True
        else:
            print(stored_password)
            print(password)
            print("fel lösenord")
            return False
    else:
        return False
