from flask import Flask, render_template, request, redirect
from os import listdir
from db_operations import fetchone, update

import psycopg2


def editProfile(username):
    img = request.form["img"]
    info = request.form["info"]
    level = request.form["level"]
    age = request.form["age"]
    asd = fetchone("select pid from registration where username = %s", [username])
    sql = "update profile set img = %s, info = %s, level = %s, age = %s where pid = %s"
    val = (img, info, level, age, asd)
    update(sql, val)

