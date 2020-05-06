from flask import Flask, render_template, request, redirect, session
import hashlib, binascii, os
from db_operations import fetchall, fetchone

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


def log_in():
    cred = []
    cred = fetchall("select username from registration", "")
    usernameList = ("".join(str(cred)))
    username = request.form["userName"]
    password = request.form["pwd"]

    if username in usernameList:
        usernameToFind = (username,)
        cred = fetchone("select password from registration where username=%s", usernameToFind)
        stored_password = cred[0]
        print(stored_password)
        print(password)
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
