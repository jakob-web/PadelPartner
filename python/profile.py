from flask import Flask, render_template, request, redirect, session
from os import listdir
from db_operations import fetchone, update
from werkzeug.utils import secure_filename
import os

import psycopg2

UPLOAD_FOLDER = '/Users/marcusasker/Downloads/Grupp09/python/static/img'
ALLOWED_EXTENSIONS = ["PNG", "JPG", "JPEG", "GIF"]


def editProfile(username):
    print(request.form)
    img = validatepicture()
    print(img)
    info = request.form["info"]
    level = request.form["level"]
    age = request.form["age"]
    asd = fetchone("select pid from registration where username = %s", [username])
    sql = "update profile set img = %s, info = %s, level = %s, age = %s where pid = %s"
    val = (img, info, level, age, asd)
    print(sql, val)
    update(sql, val)

def allowed_image(filename):
    
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in ALLOWED_EXTENSIONS:
        return True 
    else:
        return False

def validatepicture():
    name = fetchone("select pid from registration where username = %s", [session["username"]])
    for something in name:
        picturename = something

    if request.method == "POST":
        print("1")
        print(request.files)
        if request.files:
            print("2")
            image = request.files["image"]
            print(image)
            if image.filename == "":
                print("image must have a filename")
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("BAJSBAJBASJASBASJJS")
                print(image.filename)
                print("That image extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)

            print(image)
            print(image.filename)
            image.filename = str(picturename) + ".jpg"
            print(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, image.filename))

            return "static/img/uploads/" + str(image.filename)

